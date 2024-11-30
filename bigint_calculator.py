class BigInt:
    def __init__(self, value):
        # Initialize BigInt with a string or integer value
        if isinstance(value, str):
            # Handle negative numbers
            if value.startswith("-"):
                self.sign = -1
                self.digits = [int(c) for c in value[1:]]
            else:
                self.sign = 1
                self.digits = [int(c) for c in value]
        elif isinstance(value, int):
            # Handle integer values
            self.sign = 1 if value >= 0 else -1
            self.digits = [int(c) for c in str(abs(value))]
        else:
            raise TypeError("Unsupported type for BigInt")

    def __str__(self):
        # Return the string representation of the BigInt
        return ("-" if self.sign == -1 else "") + "".join(map(str, self.digits))

    def __add__(self, other):
        # Define addition operation for BigInt
        if self.sign == other.sign:
            result = BigInt._add_abs(self.digits, other.digits)
            result.sign = self.sign
        else:
            # Handle subtraction when signs differ
            if BigInt._compare_abs(self.digits, other.digits) >= 0:
                result = BigInt._sub_abs(self.digits, other.digits)
                result.sign = self.sign
            else:
                result = BigInt._sub_abs(other.digits, self.digits)
                result.sign = other.sign
        return result

    def __sub__(self, other):
        # Define subtraction operation for BigInt
        return self + BigInt("-" + str(other)) if self.sign != other.sign else self + BigInt(str(-other))

    def __mul__(self, other):
        # Define multiplication operation for BigInt
        result_sign = self.sign * other.sign
        result = BigInt._mul_abs(self.digits, other.digits)
        result.sign = result_sign
        return result

    def __floordiv__(self, other):
        # Define floor division operation for BigInt
        quotient, _ = BigInt._divmod_abs(self.digits, other.digits)
        result = BigInt("".join(map(str, quotient)))
        result.sign = self.sign * other.sign
        return result

    def __mod__(self, other):
        # Define modulus operation for BigInt
        _, remainder = BigInt._divmod_abs(self.digits, other.digits)
        result = BigInt("".join(map(str, remainder)))
        result.sign = self.sign
        return result

    def __pow__(self, other):
        # Define exponentiation operation for BigInt
        if other.sign == -1:
            raise ValueError("Exponentiation with negative powers is unsupported")
        result = BigInt(1)
        base = self
        power = other.digits[:]
        
        while power != [0]:
            if power[-1] % 2 == 1:  # Check if power is odd
                result *= base
            base *= base  # Square the base
            power = BigInt._divmod_abs(power, [2])[0]  # Halve the power
            
        return result

    def factorial(self):
        # Calculate factorial of the BigInt number
        if self.sign == -1:
            raise ValueError("Factorial is undefined for negative integers")
        
        result = BigInt(1)
        current = BigInt(1)
        
        while current <= self:
            result *= current  # Multiply current factorial value by current number
            current += BigInt(1)  # Increment current number
            
        return result

    # Helper methods for internal operations on absolute values of digits

    @staticmethod
    def _add_abs(a, b):
        # Addition of two absolute values represented as lists of digits
        result = []
        carry = 0
        
        a, b = a[::-1], b[::-1]  # Reverse lists for easier addition
        
        for i in range(max(len(a), len(b))):
            digit_a = a[i] if i < len(a) else 0
            digit_b = b[i] if i < len(b) else 0
            
            s = digit_a + digit_b + carry  # Sum digits and carry
            
            result.append(s % 10)  # Append last digit of sum to results
            carry = s // 10  # Update carry
            
        if carry:
            result.append(carry)  # Append remaining carry if exists
            
        return BigInt("".join(map(str, result[::-1])))  # Return as a new BigInt

    @staticmethod
    def _sub_abs(a, b):
        # Subtraction of two absolute values represented as lists of digits
        result = []
        borrow = 0
        
        a, b = a[::-1], b[::-1]  # Reverse lists for easier subtraction
        
        for i in range(len(a)):
            digit_a = a[i]
            digit_b = b[i] if i < len(b) else 0
            
            s = digit_a - digit_b - borrow
            
            if s < 0:
                s += 10  
                borrow = 1  
            else:
                borrow = 0
                
            result.append(s)  
        
        while len(result) > 1 and result[-1] == 0:  
            result.pop()  
            
        return BigInt("".join(map(str, result[::-1])))  

    @staticmethod
    def _mul_abs(a, b):
        # Multiplication of two absolute values represented as lists of digits
        result = [0] * (len(a) + len(b))
        
        a, b = a[::-1], b[::-1]  
        
        for i in range(len(a)):
            carry = 0
            
            for j in range(len(b)):
                result[i + j] += a[i] * b[j] + carry  
                carry = result[i + j] // 10  
                result[i + j] %= 10  
                
            if carry:
                result[i + len(b)] += carry  
                
        while len(result) > 1 and result[-1] == 0:  
            result.pop()  
            
        return BigInt("".join(map(str, result[::-1])))  

    @staticmethod
    def _divmod_abs(a, b):
        # Division and modulus of two absolute values represented as lists of digits
        if b == [0]:
            raise ZeroDivisionError("Division by zero")
        
        quotient = []
        remainder = []
        
        for digit in a:
            remainder.append(digit)
            q = 0
            
            while BigInt._compare_abs(remainder, b) >= 0:
                remainder = BigInt._sub_abs(remainder, b).digits 
                q += 1
                
            quotient.append(q)
            
        while len(quotient) > 1 and quotient[0] == 0:  
            quotient.pop(0)  
            
        return quotient, remainder  

    @staticmethod
    def _compare_abs(a, b):
        # Compare two absolute values represented as lists of digits
        if len(a) != len(b):
            return len(a) - len(b)
        
        for digit_a, digit_b in zip(a, b):
            if digit_a != digit_b:
                return digit_a - digit_b
                
        return 0  

    def __lt__(self, other):
         # Less than comparison between two BigInts 
         if self.sign != other.sign:
             return self.sign < other.sign
        
         cmp = BigInt._compare_abs(self.digits, other.digits)
         return cmp < 0 if self.sign == 1 else cmp > 0  

    def __le__(self, other):
         # Less than or equal comparison between two BigInts 
         return self < other or self == other  

    def __eq__(self, other):
         # Equality comparison between two BigInts 
         return self.sign == other.sign and self.digits == other.digits  

    def __neg__(self):
         # Negate the value of the current BigInt 
         result = BigInt(str(self))
         result.sign *= -1  
         return result  


def repl():
    print("Arbitrary-Precision Integer Calculator")
    print("Supported operations: +, -, *, /, %, **, !")
    print("Type 'exit' to quit.")
    
    while True:
         try:
             expr = input(">> ").strip() 
             if expr.lower() == "exit":
                 break
            
             # Parse and evaluate expressions based on user input 
             if "!" in expr:
                 num = BigInt(expr[:-1].strip())
                 print(num.factorial())
             elif "**" in expr:
                 base, exp = map(str.strip, expr.split("**"))
                 print(BigInt(base) ** BigInt(exp))
             elif "+" in expr:
                 a, b = map(str.strip, expr.split("+"))
                 print(BigInt(a) + BigInt(b))
             elif "-" in expr:
                 a, b = map(str.strip, expr.split("-"))
                 print(BigInt(a) - BigInt(b))
             elif "*" in expr:
                 a, b = map(str.strip, expr.split("*"))
                 print(BigInt(a) * BigInt(b))
             elif "/" in expr:
                 a, b = map(str.strip, expr.split("/"))
                 print(BigInt(a) // BigInt(b))
             elif "%" in expr:
                 a, b = map(str.strip, expr.split("%"))
                 print(BigInt(a) % BigInt(b))
             else:
                 print("Invalid input")
         except Exception as e:
             print(f"Error: {e}")


if __name__ == "__main__":
     repl() 
