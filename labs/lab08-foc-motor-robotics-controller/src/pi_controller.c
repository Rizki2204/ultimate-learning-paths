#include "pi_controller.h"

void pi_init(PIController *pi, double kp, double ki, double out_min, double out_max) {
    if (!pi) return;
    pi->kp = kp;
    pi->ki = ki;
    pi->integrator = 0.0;
    pi->out_min = out_min;
    pi->out_max = out_max;
}

void pi_reset(PIController *pi) {
    if (!pi) return;
    pi->integrator = 0.0;
}

double pi_update(PIController *pi, double setpoint, double feedback, double dt) {
    if (!pi) return 0.0;

    double error = setpoint - feedback;

    /* Proportional term */
    double p_term = pi->kp * error;

    /* Integral term with anti-windup clamping */
    pi->integrator += pi->ki * error * dt;
    if (pi->integrator > pi->out_max) pi->integrator = pi->out_max;
    if (pi->integrator < pi->out_min) pi->integrator = pi->out_min;

    double output = p_term + pi->integrator;
    if (output > pi->out_max) output = pi->out_max;
    if (output < pi->out_min) output = pi->out_min;

    return output;
}
