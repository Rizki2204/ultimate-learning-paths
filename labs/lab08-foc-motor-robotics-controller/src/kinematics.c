#include "kinematics.h"
#include <math.h>

EndEffectorPos forward_kinematics(ArmDimensions arm, JointAngles angles) {
    EndEffectorPos pos;
    double t1 = angles.theta1;
    double t12 = angles.theta1 + angles.theta2;

    pos.x = arm.l1 * cos(t1) + arm.l2 * cos(t12);
    pos.y = arm.l1 * sin(t1) + arm.l2 * sin(t12);
    return pos;
}

bool inverse_kinematics(ArmDimensions arm, EndEffectorPos target, bool elbow_up, JointAngles *out_angles) {
    if (!out_angles || arm.l1 <= 0.0 || arm.l2 <= 0.0) return false;

    double x = target.x;
    double y = target.y;
    double r_sq = x * x + y * y;

    /* Law of Cosines to find cos(theta2) */
    double D = (r_sq - arm.l1 * arm.l1 - arm.l2 * arm.l2) / (2.0 * arm.l1 * arm.l2);

    /* Check workspace reachability */
    if (D < -1.0 || D > 1.0) {
        return false; /* Target is out of reach */
    }

    double sin_t2 = sqrt(1.0 - D * D);
    if (elbow_up) {
        sin_t2 = -sin_t2;
    }

    double theta2 = atan2(sin_t2, D);
    double theta1 = atan2(y, x) - atan2(arm.l2 * sin(theta2), arm.l1 + arm.l2 * cos(theta2));

    out_angles->theta1 = theta1;
    out_angles->theta2 = theta2;
    return true;
}
