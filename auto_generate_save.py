try:
       for number in numbers:
           min_val = min(min_val, number)
           max_val = max(max_val, number)
           total += number
   except Exception as e:
       # Handle or re-raise the exception as needed
       return None, None, None  # Or raise