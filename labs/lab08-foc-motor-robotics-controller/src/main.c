#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "foc_math.h"
#include "pi_controller.h"
#include "svpwm.h"
#include "kinematics.h"

int run_foc_simulation(int num_steps, double *out_final_iq);

static int test_clarke_park(void) {
    PhaseCurrents i_abc = { 10.0, -5.0, -5.0 };
    AlphaBeta ab = clarke_transform(i_abc);

    /* For balanced three-phase: i_a = 10, i_b = -5 -> i_alpha = 10, i_beta = 0 */
    if (fabs(ab.alpha - 10.0) > 1e-4) return 1;
    if (fabs(ab.beta - 0.0) > 1e-4) return 2;

    double theta = M_PI / 4.0; /* 45 degrees */
    DQFrame dq = park_transform(ab, theta);

    /* Norm invariance: alpha^2 + beta^2 == d^2 + q^2 */
    double norm_ab = ab.alpha * ab.alpha + ab.beta * ab.beta;
    double norm_dq = dq.d * dq.d + dq.q * dq.q;
    if (fabs(norm_ab - norm_dq) > 1e-4) return 3;

    /* Inverse Park round-trip */
    AlphaBeta ab_recon = inverse_park_transform(dq, theta);
    if (fabs(ab_recon.alpha - ab.alpha) > 1e-4) return 4;
    if (fabs(ab_recon.beta - ab.beta) > 1e-4) return 5;

    return 0;
}

static int test_pi(void) {
    PIController pi;
    pi_init(&pi, 2.0, 50.0, -10.0, 10.0);

    /* Step response with setpoint 5.0, initial feedback 0.0 */
    double out1 = pi_update(&pi, 5.0, 0.0, 0.01);
    /* p_term = 10, integrator = 25 -> total 35 clamped to 10 */
    if (out1 != 10.0) return 1;

    /* Anti-windup check: integrator must not exceed out_max */
    if (pi.integrator > 10.0) return 2;

    return 0;
}

static int test_svpwm(void) {
    AlphaBeta v_ab = { 8.0, 8.0 };
    double v_dc = 24.0;
    double t_pwm = 0.0001; /* 100 microseconds */

    SVPWMResult res = svpwm_generate(v_ab, v_dc, t_pwm);

    if (res.sector < 1 || res.sector > 6) return 1;
    double sum_t = res.t1 + res.t2 + res.t0;
    if (fabs(sum_t - t_pwm) > 1e-8) return 2;

    if (res.duty.a < 0.0 || res.duty.a > 1.0) return 3;
    if (res.duty.b < 0.0 || res.duty.b > 1.0) return 4;
    if (res.duty.c < 0.0 || res.duty.c > 1.0) return 5;

    return 0;
}

static int test_kinematics(void) {
    ArmDimensions arm = { 1.0, 0.8 };
    JointAngles true_angles = { 0.5, 0.8 };

    EndEffectorPos ee = forward_kinematics(arm, true_angles);

    JointAngles ik_angles;
    if (!inverse_kinematics(arm, ee, false, &ik_angles)) return 1;

    EndEffectorPos recon_ee = forward_kinematics(arm, ik_angles);
    if (fabs(recon_ee.x - ee.x) > 1e-4) return 2;
    if (fabs(recon_ee.y - ee.y) > 1e-4) return 3;

    /* Unreachable target check (radius > l1 + l2) */
    EndEffectorPos unreachable = { 3.0, 3.0 };
    if (inverse_kinematics(arm, unreachable, false, &ik_angles)) return 4;

    return 0;
}

static int test_sim(void) {
    double final_iq = 0.0;
    run_foc_simulation(1000, &final_iq);

    /* Target is 2.0 Amperes; must have converged close to 2.0 A */
    if (fabs(final_iq - 2.0) > 0.1) return 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s [--test-clarke-park | --test-pi | --test-svpwm | --test-kinematics | --test-sim | --test-all]\n", argv[0]);
        return 0;
    }

    if (strcmp(argv[1], "--test-clarke-park") == 0) {
        int r = test_clarke_park();
        printf("clarke_park_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-pi") == 0) {
        int r = test_pi();
        printf("pi_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-svpwm") == 0) {
        int r = test_svpwm();
        printf("svpwm_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-kinematics") == 0) {
        int r = test_kinematics();
        printf("kinematics_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-sim") == 0) {
        int r = test_sim();
        printf("sim_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-all") == 0) {
        int cp = test_clarke_park();
        int pi = test_pi();
        int sv = test_svpwm();
        int km = test_kinematics();
        int sm = test_sim();
        int total = cp + pi + sv + km + sm;
        printf("{\"clarke_park\": %d, \"pi\": %d, \"svpwm\": %d, \"kinematics\": %d, \"simulation\": %d}\n",
               cp, pi, sv, km, sm);
        return total == 0 ? 0 : 1;
    }

    return 1;
}
