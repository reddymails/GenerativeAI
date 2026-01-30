
def parse_best_flights(best_flights):
    parsed = []

    for option in best_flights:
        flights = option.get("flights", [])
        layovers = option.get("layovers", [])

        segments = []
        flight_numbers = []
        delay_flag = False

        for f in flights:
            dep = f["departure_airport"]
            arr = f["arrival_airport"]

            segments.append({
                "from": dep["id"],
                "to": arr["id"],
                "depart_time": dep["time"],
                "arrive_time": arr["time"],
                "duration_min": f["duration"],
                "aircraft": f.get("airplane"),
                "flight_number": f.get("flight_number")
            })

            flight_numbers.append(f.get("flight_number"))

            if f.get("often_delayed_by_over_30_min"):
                delay_flag = True

        parsed.append({
            "price": option.get("price"),
            "currency": "INR",
            "total_duration_min": option.get("total_duration"),
            "airline": flights[0].get("airline") if flights else None,
            "stops": len(flights) - 1,
            "non_stop": len(flights) == 1,
            "flight_numbers": flight_numbers,
            "segments": segments,
            "layovers": layovers,
            "delay_risk": delay_flag,
            "booking_token": option.get("booking_token")
        })

    return parsed
