# MetricMind Query Parser

METRIC_KEYWORDS = {
    "revenue": [
        "revenue",
        "sales",
        "income",
        "earnings",
        "money made",
        "turnover"
    ],

    "cost": [
        "cost",
        "expense",
        "expenses",
        "spending"
    ],

    "profit": [
        "profit",
        "profits"
    ],

    "margin": [
        "margin",
        "profit margin"
    ]
}


REGIONS = [
    "Europe",
    "Asia",
    "North America"
]


PRODUCTS = [
    "Software",
    "Hardware",
    "Services"
]


def detect_metric(question):
    question = question.lower()

    for metric, keywords in METRIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in question:
                return metric

    return None


def detect_region(question):
    question_lower = question.lower()

    for region in REGIONS:
        if region.lower() in question_lower:
            return region

    return None


def detect_product(question):
    question_lower = question.lower()

    for product in PRODUCTS:
        if product.lower() in question_lower:
            return product

    return None


def parse_question(question):

    metric = detect_metric(question)
    region = detect_region(question)
    product = detect_product(question)

    return {
        "metric": metric,
        "region": region,
        "product": product
    }


if __name__ == "__main__":

    question = question = "How much money did we make from Europe?"

    result = parse_question(question)

    print(result)