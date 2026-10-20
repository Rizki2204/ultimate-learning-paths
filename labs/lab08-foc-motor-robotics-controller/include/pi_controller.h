#ifndef PI_CONTROLLER_H
#define PI_CONTROLLER_H

typedef struct {
    double kp;
    double ki;
    double integrator;
    double out_min;
    double out_max;
} PIController;

void pi_init(PIController *pi, double kp, double ki, double out_min, double out_max);
void pi_reset(PIController *pi);
double pi_update(PIController *pi, double setpoint, double feedback, double dt);

#endif /* PI_CONTROLLER_H */
