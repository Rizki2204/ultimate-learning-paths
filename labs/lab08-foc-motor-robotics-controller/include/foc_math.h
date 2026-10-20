#ifndef FOC_MATH_H
#define FOC_MATH_H

#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#define ONE_BY_SQRT3 0.5773502691896257
#define TWO_BY_SQRT3 1.1547005383792515
#define SQRT3        1.7320508075688772

typedef struct {
    double a;
    double b;
    double c;
} PhaseCurrents;

typedef struct {
    double alpha;
    double beta;
} AlphaBeta;

typedef struct {
    double d;
    double q;
} DQFrame;

typedef struct {
    double a;
    double b;
    double c;
} PWMDutyCycles;

AlphaBeta clarke_transform(PhaseCurrents current);
DQFrame park_transform(AlphaBeta ab, double theta_e);
AlphaBeta inverse_park_transform(DQFrame dq, double theta_e);

#endif /* FOC_MATH_H */
