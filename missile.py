import math

G = 6.67408e-11
MASS_E = 5.972e24
RADIUS_E = 6371000.0
SAMPLE_TO_PRINT = 10000
ATMOSPHERE = 100000.00
GOLDEN_RATIO = (math.sqrt(5) + 1) / 2


def get_gravitational_acceleration(altitude):
    altitude = float(altitude)
    return -1.0 * float(G * MASS_E) / float(RADIUS_E + altitude)**2.0


def calc_reenty(altitude, velocity=0.0, dt=.01, target_altitude=0.0):
    # cast everything to floats cause python sucks
    altitude, velocity, dt, target_altitude = float(
        altitude), float(velocity), float(dt), float(target_altitude)
    total_time = 0.0
    sample = 0

    # repeat until at target
    while(altitude >= target_altitude):

        a_g = get_gravitational_acceleration(altitude)
        velocity = velocity + a_g * dt
        altitude = altitude + velocity * dt + 1.0 / 2.0 * a_g * dt**2.0
        total_time = total_time + dt
        sample += 1
        '''
        if sample % SAMPLE_TO_PRINT == 0:
            print "Acceleration (m/s^2)", a_g, "Altitude", altitude, \
                "Velocity (m/s)", velocity, "Time Elapsed (s)", total_time, \
                "Time Elapsed (min)", total_time / 60.0
        '''
    # we're done! print results
    '''
    print "Boom", "Took", sample, "samples. Missile at", altitude, "m"
    print "Acceleration (m/s^2)", a_g, "Altitude", altitude, \
        "Velocity (m/s)", velocity, "Time Elapsed (s)", total_time, \
        "Time Elapsed (min)", total_time / 60.0
    '''
    return total_time


def gss(f, a, b, tol=1e-5):
    '''
    golden section search
    to find the minimum of f on [a,b]
    f: a strictly unimodal function on [a,b]

    example:
    >>> f = lambda x: (x-2)**2
    >>> x = gss(f, 1, 5)
    >>> x
    2.000009644875678

    '''
    c = b - (b - a) / GOLDEN_RATIO
    d = a + (b - a) / GOLDEN_RATIO
    while abs(c - d) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c

        # we recompute both c and d here to avoid loss of precision which may
        # lead to incorrect results or infinite loop
        c = b - (b - a) / GOLDEN_RATIO
        d = a + (b - a) / GOLDEN_RATIO

    return (b + a) / 2


def altitude_from_time(time_seconds):
    def f(x):
        return abs(calc_reenty(x) - time_seconds)
    return gss(f, 0, 10000e3)

target_time = 30/2.0 * 60.0
altitude_guess = altitude_from_time(target_time)
altitude_guess_km = altitude_guess/1000.0
print "Target Time(s)", target_time, "Required altitude (km)", altitude_guess_km

altitude = 2155e3
print "Altitude", altitude
print "Reentry", calc_reenty(altitude, 0.0, .01, ATMOSPHERE)
print "Impact no aero", calc_reenty(altitude)
