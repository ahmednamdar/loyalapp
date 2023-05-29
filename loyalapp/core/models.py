from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.db import models
from decimal import Decimal
import random
from django.db import models


# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle = models.CharField(max_length=30)


class Group(models.Model):
    name = models.CharField(max_length=100)
    discount_percent = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name




class customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    credit = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    identity = models.PositiveIntegerField(default=0, editable=False)

    
    birthday = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name+' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.identity == 0:
            self.identity = random.randint(100000, 999999)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.quantity) + " " + self.product

    def _calculate_total(self):
        return self.price * self.quantity
    total = property(_calculate_total)

# class Order(models.Model):
  #  customer = models.ForeignKey(customer, on_delete=models.CASCADE)

  #  items = models.ManyToManyField(OrderItem)

  #  applied = models.BooleanField(null=True,default=True,editable=False)
    # total = models.DecimalField(max_digits=10, decimal_places=2,null=True)

 #   date_placed = models.DateTimeField(auto_now_add=True)

  #  def _calculate_total(self):
  #      sumof = sum(item.total for item in self.items.all())
  #      if self.applied:
  #          self.customer.credit = Decimal(self.customer.credit) + Decimal((sumof * self.customer.group.discount_percent/100))
   #         self.applied = False
   #         self.save()
   #         self.customer.save()

    #    return sumof

    # total = property(_calculate_total)

   # def save(self, *args, **kwargs):

    #    self.customer.credit = Decimal(self.customer.credit) + Decimal((sumof*self.customer.group.discount_percent/100))
    #    self.customer.save()
    # print(self.items)
    # # self.total = 10 - self.customer.credit
    # if self.customer.group:
    #     self.total = self.total*Decimal((100 - self.customer.group.discount_percent) / 100)
    # self.customer.credit = ((self.total*self.customer.group.discount_percent/100) +(self.customer.credit))
    # sumof = sum(item.total for item in self.items.all())
    # self.customer.credit = Decimal(self.customer.credit) + Decimal((sumof*self.customer.group.discount_percent/100))
    # self.customer.save()
    # super().save(*args, **kwargs)


#class Invoice(models.Model):
  #  tableNumber = models.IntegerField()
  #  totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
 #   date = models.DateTimeField(auto_now_add=True)
 #   invoiceNumber = models.IntegerField(primary_key=True, editable=True)
 #   def __str__(self):
 #       return str(self.invoiceNumber)
#
#    payWithCredit = models.BooleanField()
class Order(models.Model):
    customer = models.ForeignKey('customer', on_delete=models.CASCADE)

    tableNumber = models.IntegerField()
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    invoiceNumber = models.IntegerField()
    payWithCredit = models.BooleanField()
    creditTocut =models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)

    def get_credit(self):
        return self.customer.credit

    # total = models.DecimalField(
    #     max_digits=10, decimal_places=2, null=True,)


    def save(self, *args, **kwargs):
        if self.creditTocut == None :
            self.creditTocut = 0 
        holder = self.totalPrice
        print(self.creditTocut)
        if self.payWithCredit:
            if  self.creditTocut > 0 and self.creditTocut < self.customer.credit :

                self.totalPrice = self.totalPrice - self.creditTocut
                self.customer.credit = self.customer.credit - self.creditTocut
            elif (self.totalPrice >= self.customer.credit):
                self.totalPrice = self.totalPrice - self.customer.credit
                self.customer.credit = 0
            elif (self.totalPrice < self.customer.credit):
                
                self.totalPrice = 0
                self.customer.credit = self.customer.credit - self.totalPrice
        # else:
            # self.totalPrice = self.totalPrice
        if not self.payWithCredit:
            self.customer.credit = Decimal(self.customer.credit) + Decimal(
                (holder*self.customer.group.discount_percent/100))
        self.customer.save()
        super().save(*args, **kwargs)



    

# class OrderItemRelation(models.Model):
#     item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
