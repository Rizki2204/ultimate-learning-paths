#include "foc_math.h"

AlphaBeta clarke_transform(PhaseCurrents current) {
    AlphaBeta ab;
    ab.alpha = current.a;
    ab.beta = ONE_BY_SQRT3 * (current.a + 2.0 * current.b);
    return ab;
}

DQFrame park_transform(AlphaBeta ab, double theta_e) {
    DQFrame dq;
    double sin_t = sin(theta_e);
    double cos_t = cos(theta_e);

    dq.d =  ab.alpha * cos_t + ab.beta * sin_t;
    dq.q = -ab.alpha * sin_t + ab.beta * cos_t;
    return dq;
}

AlphaBeta inverse_park_transform(DQFrame dq, double theta_e) {
    AlphaBeta ab;
    double sin_t = sin(theta_e);
    double cos_t = cos(theta_e);

    ab.alpha = dq.d * cos_t - dq.q * sin_t;
    ab.beta  = dq.d * sin_t + dq.q * cos_t;
    return ab;
}
