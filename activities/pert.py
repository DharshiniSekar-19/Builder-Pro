import math

class PERTAnalyzer:
    @staticmethod
    def calculate(optimistic, most_likely, pessimistic):
        expected = (optimistic + 4 * most_likely + pessimistic) / 6
        variance = ((pessimistic - optimistic) / 6) ** 2
        std_dev = math.sqrt(variance)
        return {
            'expected_duration': round(expected, 2),
            'variance': round(variance, 4),
            'standard_deviation': round(std_dev, 2),
        }

    @staticmethod
    def probability(target_days, expected_duration, std_dev):
        if std_dev == 0:
            return 100.0 if target_days >= expected_duration else 0.0
        z = (target_days - expected_duration) / std_dev
        probability = PERTAnalyzer._normal_cdf(z) * 100
        return round(probability, 2)

    @staticmethod
    def _normal_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
