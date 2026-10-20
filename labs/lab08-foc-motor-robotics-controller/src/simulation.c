#include <stdio.h>
#include "foc_math.h"
#include "pi_controller.h"
#include "svpwm.h"

int run_foc_simulation(int num_steps, double *out_final_iq) {
    PIController pi_d;
    PIController pi_q;

    pi_init(&pi_d, 5.0, 100.0, -24.0, 24.0);
    pi_init(&pi_q, 5.0, 100.0, -24.0, 24.0);

    double dt = 0.0001; /* 100 microseconds (10 kHz control loop) */
    double theta_e = 0.0;
    double omega_e = 50.0; /* rad/s electrical speed */

    /* Motor currents */
    double id = 0.0;
    double iq = 0.0;

    double id_target = 0.0;
    double iq_target = 2.0; /* 2 Amperes target torque current */

    for (int step = 0; step < num_steps; ++step) {
        theta_e += omega_e * dt;
        if (theta_e > 2.0 * M_PI) theta_e -= 2.0 * M_PI;

        /* PI control update */
        double vd = pi_update(&pi_d, id_target, id, dt);
        double vq = pi_update(&pi_q, iq_target, iq, dt);

        /* Inverse Park to alpha-beta */
        DQFrame v_dq = { vd, vq };
        AlphaBeta v_ab = inverse_park_transform(v_dq, theta_e);

        /* SVPWM modulation */
        svpwm_generate(v_ab, 24.0, dt);

        /* Motor electrical model update (R=1.0, L=0.002) */
        double R = 1.0;
        double L = 0.002;
        double did_dt = (vd - R * id) / L;
        double diq_dt = (vq - R * iq) / L;

        id += did_dt * dt;
        iq += diq_dt * dt;
    }

    if (out_final_iq) *out_final_iq = iq;
    return 0;
}
