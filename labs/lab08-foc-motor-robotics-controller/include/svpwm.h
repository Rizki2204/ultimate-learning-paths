#ifndef SVPWM_H
#define SVPWM_H

#include "foc_math.h"

typedef struct {
    int sector;
    double t1;
    double t2;
    double t0;
    PWMDutyCycles duty;
} SVPWMResult;

SVPWMResult svpwm_generate(AlphaBeta v_alpha_beta, double v_dc, double t_pwm);

#endif /* SVPWM_H */
