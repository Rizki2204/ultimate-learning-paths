#include "svpwm.h"

SVPWMResult svpwm_generate(AlphaBeta v_alpha_beta, double v_dc, double t_pwm) {
    SVPWMResult res;
    if (v_dc <= 0.0 || t_pwm <= 0.0) {
        res.sector = 1;
        res.t1 = 0; res.t2 = 0; res.t0 = t_pwm;
        res.duty.a = 0.5; res.duty.b = 0.5; res.duty.c = 0.5;
        return res;
    }

    double v_mag = sqrt(v_alpha_beta.alpha * v_alpha_beta.alpha +
                        v_alpha_beta.beta  * v_alpha_beta.beta);

    double theta = atan2(v_alpha_beta.beta, v_alpha_beta.alpha);
    if (theta < 0.0) {
        theta += 2.0 * M_PI;
    }

    int sector = (int)(theta / (M_PI / 3.0)) + 1;
    if (sector > 6) sector = 6;
    res.sector = sector;

    double alpha_rel = theta - (sector - 1) * (M_PI / 3.0);

    double t1 = SQRT3 * (v_mag / v_dc) * t_pwm * sin(M_PI / 3.0 - alpha_rel);
    double t2 = SQRT3 * (v_mag / v_dc) * t_pwm * sin(alpha_rel);

    if (t1 < 0.0) t1 = 0.0;
    if (t2 < 0.0) t2 = 0.0;

    /* Overmodulation saturation scaling */
    if (t1 + t2 > t_pwm) {
        double scale = t_pwm / (t1 + t2);
        t1 *= scale;
        t2 *= scale;
    }

    double t0 = t_pwm - (t1 + t2);
    res.t1 = t1;
    res.t2 = t2;
    res.t0 = t0;

    double half_t0 = t0 / 2.0;
    double ta = 0.0, tb = 0.0, tc = 0.0;

    switch (sector) {
        case 1:
            ta = half_t0 + t1 + t2;
            tb = half_t0 + t2;
            tc = half_t0;
            break;
        case 2:
            ta = half_t0 + t1;
            tb = half_t0 + t1 + t2;
            tc = half_t0;
            break;
        case 3:
            ta = half_t0;
            tb = half_t0 + t1 + t2;
            tc = half_t0 + t2;
            break;
        case 4:
            ta = half_t0;
            tb = half_t0 + t1;
            tc = half_t0 + t1 + t2;
            break;
        case 5:
            ta = half_t0 + t2;
            tb = half_t0;
            tc = half_t0 + t1 + t2;
            break;
        case 6:
        default:
            ta = half_t0 + t1 + t2;
            tb = half_t0;
            tc = half_t0 + t1;
            break;
    }

    res.duty.a = ta / t_pwm;
    res.duty.b = tb / t_pwm;
    res.duty.c = tc / t_pwm;

    return res;
}
