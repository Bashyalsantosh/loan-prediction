"""
Kafka Producer Simulator for NRB Loan Stream
"""

import json
import time
import random
from kafka import KafkaProducer

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def generate_loan_payload(seq_id):
    return {
        "loan_id": f"L-NRB-{1000 + seq_id}",
        "applicant_income": random.randint(35000, 180000),
        "coapplicant_income": random.choice([0, 15000, 25000, 40000]),
        "loan_amount": random.randint(200000, 5000000),
        "credit_score": random.randint(520, 820),
        "collateral_value": random.randint(800000, 8000000),
        "timestamp": int(time.time())
    }

if __name__ == "__main__":
    print("📡 Initializing Kafka Loan Data Stream Producer...")
    try:
        producer = create_kafka_producer()
        print("✅ Connected to Kafka Broker at localhost:9092")
        
        for i in range(1, 101):
            payload = generate_loan_payload(i)
            producer.send('nrb_loans', value=payload)
            print(f"🚀 Sent [{i}/100]: {payload['loan_id']} - NPR {payload['loan_amount']:,}")
            time.sleep(0.1)
            
        producer.flush()
        print("\n✨ Stream Simulation Batch Complete!")
    except Exception as e:
        print(f"❌ Failed to push streaming payload: {e}")
