#ifndef KINEMATICS_H
#define KINEMATICS_H

#include <stdbool.h>

typedef struct {
    double l1;
    double l2;
} ArmDimensions;

typedef struct {
    double theta1;
    double theta2;
} JointAngles;

typedef struct {
    double x;
    double y;
} EndEffectorPos;

EndEffectorPos forward_kinematics(ArmDimensions arm, JointAngles angles);
bool inverse_kinematics(ArmDimensions arm, EndEffectorPos target, bool elbow_up, JointAngles *out_angles);

#endif /* KINEMATICS_H */
