import json
import requests

def run_evals():
    with open("evals/cases.json", "r", encoding="utf-8") as f:
        cases = json.load(f)

    score = 0
    failed_cases = []
    url = "http://localhost:8000/normalize_car_ad"

    print("-----Running evaluations-----")
    for i, case in enumerate(cases):
        payload = {"text" : case ["input"]}
        try:
            response = requests.post(url, json = payload)
            response.raise_for_status()
            result = response.json()

            brand_match = result["brand"] == case["expected_brand"]
            transmission_match = result["transmission"] == case["expected_transmission"]

            if brand_match and transmission_match:
                score += 1
                print(f"Case {i + 1}: Passed")
            else:
                print(f"Case {i+1} Failed. Expected {case['expected_brand']}/{case['expected_transmission']}, got {result['brand']}/{result['transmission']}")
                failed_cases.append(i+1) 
        except Exception as e:
            print(f"Case {i+1} Failed with error: {e}")
            failed_cases.append(i+1)

    print("-----Evaluation Summary-----")
    print(f"Total Cases: {len(cases)}")
    print(f"Passed Cases: {score}")
    print(f"Failed Cases: {len(failed_cases)}")

if __name__ == "__main__":
    run_evals()