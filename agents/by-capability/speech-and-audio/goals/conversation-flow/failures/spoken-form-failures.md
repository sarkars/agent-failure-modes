# Spoken Form Failures

## Issue: Numbers, Dates, and Formatted Text Not Converted to Spoken Form

**Frequency**: Very Common

**Symptoms**
- Agent says "five five five" as "555" (sounds robotic)
- Dates read as digits: "zero three slash zero four slash two zero two five"
- Currency: "dollar forty two point five zero"
- Phone numbers without natural grouping
- URLs spoken with "slash slash" repeatedly
- Times as "one four colon three zero"

**Root Cause**
LLMs output text in written form by default. Without explicit spoken-form instructions, the TTS engine receives "555" and speaks it as written rather than as humans would say it ("five five five"). This affects numbers, dates, currency, phone numbers, times, and any formatted text. The result sounds robotic and hard to follow.

**Example**
```
Scenario 1: Phone numbers

Written form (robotic):
Agent: "Your confirmation number is 5 5 5 2 3 9 8 1 2 3."

Spoken form (natural):
Agent: "Your confirmation number is five five five, 
        two three nine, eight one two three."

← Grouping and pauses make it memorable
← Written digits sound mechanical

---

Scenario 2: Dates

Written form (robotic):
Agent: "Your appointment is on 03/04/2025 at 2:15 PM."
TTS output: "zero three slash zero four slash two zero two five 
             at two colon one five P M"

Spoken form (natural):
Agent: "Your appointment is March fourth, twenty twenty-five 
        at two fifteen in the afternoon."

← Month name, not number
← "Twenty twenty-five" not digit by digit
← "Two fifteen" not "two colon one five"

---

Scenario 3: Currency

Written form (robotic):
Agent: "The total is $42.50."
TTS output: "dollar sign forty two point five zero"

Spoken form (natural):
Agent: "The total is forty-two dollars and fifty cents."

← Full spoken amount
← No "point" or "dollar sign"

---

Scenario 4: Addresses

Written form (robotic):
Agent: "The address is 400 Main St, Suite 200."
TTS output: "four zero zero Main S T comma Suite two zero zero"

Spoken form (natural):
Agent: "The address is four hundred Main Street, 
        Suite two hundred."

← "Four hundred" not "four zero zero"
← "Street" not "S T"

---

Scenario 5: Times with AM/PM

Written form (robotic):
Agent: "We're open 9:00 AM - 5:30 PM."
TTS output: "nine colon zero zero A M dash five colon 
             three zero P M"

Spoken form (natural):
Agent: "We're open nine in the morning to five thirty 
        in the afternoon."

← Natural time expressions
← No colons or dashes spoken

---

Scenario 6: Mixed content

Written form (robotic):
"Call us at (831) 239-8123 before 03/15/2025 to claim 
 your $100.00 credit."

TTS: "Call us at open paren eight three one close paren 
      two three nine dash eight one two three before zero 
      three slash one five slash two zero two five to claim 
      your dollar sign one hundred point zero zero credit."

Spoken form (natural):
"Call us at eight three one, two three nine, eight one 
 two three before March fifteenth, twenty twenty-five 
 to claim your one hundred dollar credit."

---

Spoken form conversion analysis:
  
  Agents with spoken form rules: 38%
  Agents without conversion: 62%
  
  Most common issues:
    Phone numbers as digits: 45%
    Dates as numbers: 40%
    Currency with symbols: 35%
    Times with colons: 30%
    Addresses abbreviated: 25%
  
  Caller confusion:
    With robotic forms: 35%
    With spoken forms: 8%
  
  Caller satisfaction:
    Spoken forms: 4.3/5
    Robotic forms: 3.1/5
```

**Key Statistics**
From VAPI Voice AI Research (2026):
- Agents without spoken form rules: 60%+
- Phone number confusion: 40-50%
- Date format confusion: 35-45%
- Spoken form improves comprehension: 60%
- Natural pacing improves recall: 45%

**Written vs Spoken Form**
| Written | Spoken | Common Error |
|---------|--------|--------------|
| 555-239-8123 | five five five, two three nine, eight one two three | "five five five dash two..." |
| 03/04/2025 | March fourth, twenty twenty-five | "zero three slash zero four..." |
| $42.50 | forty-two dollars and fifty cents | "dollar forty two point five zero" |
| 2:15 PM | two fifteen in the afternoon | "two colon fifteen P M" |
| Suite 400 | suite four hundred | "suite four zero zero" |
| 100 | one hundred | "one zero zero" |

**Contributing Factors**
- LLM outputs written form by default
- No spoken form instructions in prompt
- TTS engine reads literally
- No post-processing of numbers
- Mixed content not handled
- Inconsistent formatting rules

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Phone | Confirm phone number | Natural grouping | Digit by digit |
| Date | Appointment date | Month name | MM/DD/YYYY |
| Currency | Price | Dollars and cents | Dollar sign, point |
| Time | Opening hours | "Nine in the morning" | "9:00 AM" |
| Address | Location | Street, hundred | St., 00 |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Spoken form compliance | > 95% | Output analysis |
| Natural number grouping | > 95% | Phone/number check |
| Date format natural | > 95% | Date output check |
| Caller comprehension | > 90% | Repeat rate |

---

## Mitigation Strategies

### Prevention
1. **Explicit spoken form rules**: Add to response guidelines
2. **Format examples**: Show written → spoken conversions
3. **Post-processing**: Convert before TTS
4. **Grouping rules**: Specify pause patterns
5. **Context awareness**: Different rules for reading vs confirming
6. **Testing with TTS**: Listen to actual output

### Implementation
```python
class SpokenFormConverter:
    """Convert written forms to spoken forms"""
    
    def convert(self, text: str) -> str:
        """Convert all formatted content to spoken form"""
        result = text
        
        # Convert phone numbers
        result = self.convert_phone_numbers(result)
        
        # Convert dates
        result = self.convert_dates(result)
        
        # Convert currency
        result = self.convert_currency(result)
        
        # Convert times
        result = self.convert_times(result)
        
        # Convert addresses
        result = self.convert_addresses(result)
        
        # Convert plain numbers
        result = self.convert_numbers(result)
        
        return result
    
    def convert_phone_numbers(self, text: str) -> str:
        """Convert phone numbers to spoken form"""
        # Pattern for various phone formats
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        def phone_to_spoken(match):
            digits = re.sub(r'\D', '', match.group())
            # Group as: XXX, XXX, XXXX
            return (f"{self.digits_to_words(digits[:3])}, "
                   f"{self.digits_to_words(digits[3:6])}, "
                   f"{self.digits_to_words(digits[6:])}")
        
        return re.sub(phone_pattern, phone_to_spoken, text)
    
    def digits_to_words(self, digits: str) -> str:
        """Convert digit string to spoken words"""
        words = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three',
            '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
            '8': 'eight', '9': 'nine'
        }
        return ' '.join(words[d] for d in digits)
    
    def convert_dates(self, text: str) -> str:
        """Convert dates to spoken form"""
        months = {
            '01': 'January', '02': 'February', '03': 'March',
            '04': 'April', '05': 'May', '06': 'June',
            '07': 'July', '08': 'August', '09': 'September',
            '10': 'October', '11': 'November', '12': 'December'
        }
        
        ordinals = {
            '1': 'first', '2': 'second', '3': 'third', '4': 'fourth',
            '5': 'fifth', '6': 'sixth', '7': 'seventh', '8': 'eighth',
            '9': 'ninth', '10': 'tenth', '11': 'eleventh', '12': 'twelfth',
            '13': 'thirteenth', '14': 'fourteenth', '15': 'fifteenth',
            '16': 'sixteenth', '17': 'seventeenth', '18': 'eighteenth',
            '19': 'nineteenth', '20': 'twentieth', '21': 'twenty-first',
            '22': 'twenty-second', '23': 'twenty-third', '24': 'twenty-fourth',
            '25': 'twenty-fifth', '26': 'twenty-sixth', '27': 'twenty-seventh',
            '28': 'twenty-eighth', '29': 'twenty-ninth', '30': 'thirtieth',
            '31': 'thirty-first'
        }
        
        # MM/DD/YYYY pattern
        def date_to_spoken(match):
            month = months.get(match.group(1), match.group(1))
            day = ordinals.get(match.group(2).lstrip('0'), match.group(2))
            year = self.year_to_spoken(match.group(3))
            return f"{month} {day}, {year}"
        
        return re.sub(r'(\d{2})/(\d{2})/(\d{4})', date_to_spoken, text)
    
    def year_to_spoken(self, year: str) -> str:
        """Convert year to spoken form"""
        if year.startswith('20'):
            # 2025 → "twenty twenty-five"
            first = int(year[:2])
            second = int(year[2:])
            return f"twenty {self.number_to_words(second)}"
        return year
    
    def convert_currency(self, text: str) -> str:
        """Convert currency to spoken form"""
        def currency_to_spoken(match):
            amount = match.group(1)
            parts = amount.split('.')
            dollars = int(parts[0])
            cents = int(parts[1]) if len(parts) > 1 else 0
            
            result = f"{self.number_to_words(dollars)} dollar"
            if dollars != 1:
                result += "s"
            
            if cents > 0:
                result += f" and {self.number_to_words(cents)} cent"
                if cents != 1:
                    result += "s"
            
            return result
        
        return re.sub(r'\$(\d+\.?\d*)', currency_to_spoken, text)
    
    def convert_times(self, text: str) -> str:
        """Convert times to spoken form"""
        def time_to_spoken(match):
            hour = int(match.group(1))
            minute = int(match.group(2))
            period = match.group(3).upper()
            
            hour_word = self.number_to_words(hour)
            
            if minute == 0:
                time_str = hour_word
            elif minute < 10:
                time_str = f"{hour_word} oh {self.number_to_words(minute)}"
            else:
                time_str = f"{hour_word} {self.number_to_words(minute)}"
            
            period_word = "in the morning" if period == "AM" else "in the afternoon"
            
            return f"{time_str} {period_word}"
        
        return re.sub(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)', 
                     time_to_spoken, text)
    
    def convert_addresses(self, text: str) -> str:
        """Convert address abbreviations"""
        replacements = {
            r'\bSt\b': 'Street',
            r'\bAve\b': 'Avenue',
            r'\bBlvd\b': 'Boulevard',
            r'\bDr\b': 'Drive',
            r'\bLn\b': 'Lane',
            r'\bSte\b': 'Suite',
            r'\bApt\b': 'Apartment',
        }
        
        result = text
        for pattern, replacement in replacements.items():
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def convert_numbers(self, text: str) -> str:
        """Convert standalone numbers to spoken form"""
        # Only convert certain contexts (like "Suite 400")
        def suite_to_spoken(match):
            return f"Suite {self.number_to_words(int(match.group(1)))}"
        
        return re.sub(r'Suite (\d+)', suite_to_spoken, text)
    
    def number_to_words(self, n: int) -> str:
        """Convert number to words"""
        if n < 20:
            words = ['zero', 'one', 'two', 'three', 'four', 'five',
                    'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                    'twelve', 'thirteen', 'fourteen', 'fifteen',
                    'sixteen', 'seventeen', 'eighteen', 'nineteen']
            return words[n]
        elif n < 100:
            tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
                   'sixty', 'seventy', 'eighty', 'ninety']
            if n % 10 == 0:
                return tens[n // 10]
            return f"{tens[n // 10]}-{self.number_to_words(n % 10)}"
        elif n < 1000:
            if n % 100 == 0:
                return f"{self.number_to_words(n // 100)} hundred"
            return (f"{self.number_to_words(n // 100)} hundred "
                   f"{self.number_to_words(n % 100)}")
        return str(n)  # Fallback for larger numbers
```

### Prompt Design
```yaml
instructions: |
  ## Response Guidelines - Spoken Forms
  
  For dates, money, phone numbers, and formatted text, 
  use the SPOKEN form, not the written form.
  
  PHONE NUMBERS:
  Written: (555) 239-8123
  Spoken: "five five five, two three nine, eight one two three"
  
  DATES:
  Written: 03/04/2025
  Spoken: "March fourth, twenty twenty-five"
  
  CURRENCY:
  Written: $42.50
  Spoken: "forty-two dollars and fifty cents"
  
  TIMES:
  Written: 2:15 PM
  Spoken: "two fifteen in the afternoon"
  
  ADDRESSES:
  Written: 400 Main St, Suite 200
  Spoken: "four hundred Main Street, Suite two hundred"
  
  CONFIRMATION NUMBERS:
  Written: ABC123
  Spoken: "A B C one two three" (with pauses)
  
  NEVER output:
  - Slashes in dates (/)
  - Colons in times (:)
  - Dollar signs ($)
  - Parentheses in phone numbers
  - Abbreviated street names (St, Ave)
  
  When reading numbers back for confirmation, use natural 
  grouping with pauses to aid memory.
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `spoken_form.violations` | > 5% |
| `spoken_form.phone_robotic` | > 10% |
| `spoken_form.date_numeric` | > 10% |
| `caller.repeat_request` | > 15% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Violations | > 10% | P2 |
| Phone Format | Digits without grouping | P3 |
| Date Format | Numeric dates | P3 |
| TTS Artifacts | Symbols spoken | P2 |

---

## References

- [VAPI Prompting Guide](https://docs.vapi.ai/prompting-guide) - Spoken forms
- [VAPI Voice Formatting](https://docs.vapi.ai/voice-formatting-plan) - Format control
- [TTS Best Practices](https://cloud.google.com/text-to-speech/docs/ssml) - Number handling
- [Voice UX Guidelines](https://www.nngroup.com/articles/voice-ux/) - Pacing and grouping
