from abc import ABC, abstractmethod
class Order:

    def __init__(self):
        self.items=[]
        self.quantities=[]
        self.prices=[]
        self.status="open"

    def add_item(self,item, quantity,price):
        self.items.append(item)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total=0
        for i in range(len(self.items)):
            total+=self.quantities[i]*self.prices[i]
        return total

# abstract class are mainly about dependency inversion 
# they are also handy with Liskov substitution and open/closed principle   
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self,order:Order):
         pass
    
class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self):
        pass

class AuthorizerSMS(Authorizer):
    def __init__(self):
        self.authorized=False

    def confirm_authorization(self,code):
        print(f"Authorized with the SMS code: {code}")
        self.authorized=True

    def is_authorized(self):
        return self.authorized

class NotARobot(Authorizer):
    def __init__(self):
        self.authorized=False

    def not_a_robot(self):
        print("Confirming that I am not a robot.")
        self.authorized=True

    def is_authorized(self):
        return self.authorized
    
class PaymentProcessorDebit(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code=security_code
        self.verified=False

    def pay(self,order:Order):
        print(f"Processing payment method: debit")
        print(f"Verifying the security code:{self.security_code}")
        order.status="closed"

class PaymentProcessorCredit(PaymentProcessor):
    # composition and multi level inheritance are about interface segregation 
    def __init__(self, security_code, authorizer:Authorizer):
        self.security_code=security_code
        self.authorizer=authorizer

    def pay(self,order:Order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized.")
        print(f"Processing payment method: credit")
        print(f"Verifying the security code: {self.security_code}")
        order.status="closed"  

# adding a new payment method by adding a new subclass
class PaymentProcessorPaypal(PaymentProcessor):
    def __init__(self, email, authorizer:Authorizer):
        self.email=email
        self.authorizer=authorizer
    
    def pay(self,order:Order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized.")
        print(f"Processing payment method: paypal")
        print(f"Verifying the security code::{self.email}")
        order.status="closed"
            

if __name__=='__main__':
    
    order=Order()
    order.add_item("mouse",3,100)
    order.add_item("screen",1,900)
    order.add_item("antivirus",1,200)
    print(f"Total cost: {order.total_price()}")
    print(f"Order status:{order.status}")
    print('\n')

    try:
        # authorizer=AuthorizerSMS()
        # authorizer.confirm_authorization("2234")
        authorizer=NotARobot()
        authorizer.not_a_robot()
        processor=PaymentProcessorCredit("8765", authorizer)
        processor.pay(order)
    except Exception as e:
        print(e)

    print(f"Order status:{order.status}")
