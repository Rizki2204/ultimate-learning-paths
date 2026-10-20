#include <stdio.h>
#include <math.h>

/*
 * Field-Oriented Control (FOC) Starter Scaffolding
 *
 * Exercise Instructions:
 * Implement Clarke transform (abc -> alpha, beta),
 * Park transform (alpha, beta -> d, q), and inverse Park.
 */

#define ONE_BY_SQRT3 0.5773502691896257

void starter_clarke(double ia, double ib, double *out_alpha, double *out_beta) {
    *out_alpha = ia;
    *out_beta = ONE_BY_SQRT3 * (ia + 2.0 * ib);
}

void starter_park(double alpha, double beta, double theta, double *out_d, double *out_q) {
    double s = sin(theta);
    double c = cos(theta);
    *out_d =  alpha * c + beta * s;
    *out_q = -alpha * s + beta * c;
}

int main(void) {
    double ia = 10.0, ib = -5.0;
    double alpha = 0.0, beta = 0.0;
    starter_clarke(ia, ib, &alpha, &beta);

    double d = 0.0, q = 0.0;
    starter_park(alpha, beta, 0.0, &d, &q);

    printf("Starter FOC: alpha=%.2f, beta=%.2f -> d=%.2f, q=%.2f\n", alpha, beta, d, q);
    return 0;
}
