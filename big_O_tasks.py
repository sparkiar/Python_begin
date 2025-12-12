# 1 task
def check_is_palindrome(string: str) -> bool:
    string = ''.join((string.lower().split()))
    if string == string[::-1]:
        return True
    else:
        return False

string = 'race car'
string_1 = 'racing'
print(check_is_palindrome(string))
print(check_is_palindrome(string_1))

# task 2
def two_sum_sorted(list: list[int], target: int) -> list[int]|int:
    our_list = list
    left, right = 0, len(our_list)-1
    while left < right:
        our_sum = our_list[left] + our_list[right]
        if our_sum == target:
            return [our_list[left], our_list[right]]
        elif our_sum < target:
            left += 1
        else:
            right -= 1

    return -1


my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(two_sum_sorted(my_list, 19))


# task 3
def max_profit(prices: list[int]) -> int:
    if not prices or len(prices) < 2:
        return 0
    min_price = prices[0]
    profit = 0
    for price in prices[1:]:
        if price < min_price:
            min_price = price
        potential_profit = price - min_price
        if potential_profit > profit:
            profit = potential_profit
    return profit

prices = [7, 1, 322, 4,5, 674, 35, 785 , 56, 858, 1]
print(max_profit(prices))


# task 4
def move_zero_to_end(list: list) -> None:
    counts = 0
    for i in range(len(list)):
        if list[i] != 0:

            list[counts] = list[i]
            counts += 1
    for i in range(counts, len(list)):
        my_list[i] = 0


my_list = [1, 0, 34, 23, 1, 4, 0, 64, 3, 0, 1]
move_zero_to_end(my_list)
print(my_list)


# task 5
def find_single_num(list:list) -> int:
    result = 0
    for num in list:
        result ^= num
    return result

nums = [1, 2, 3, 4, 4, 2, 1]
print(find_single_num(nums))


# task 6
def sum_of_numbers(list:list, target:int):
    list.sort()
    result = []
    for i in range(len(list)-2):
        if i > 0 and list[i]== list[i-1]:
            continue
        left, right = i+1, len(list)-1
        while left < right:
            current_sum=list[left]+list[right]+list[i]
            if current_sum==target:
                result.append([list[i], list[right], list[left]])
                while left < right and list[left]==list[left+1]:
                    left += 1
                while left < right and list[right]==list[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum>target:
                right -= 1
            else:
                left += 1
    return result

my_list = [-1, -1, 2, 0 , 4, 2, 3]
print(sum_of_numbers(my_list, 5))


# task 7
def bubble_sort(list:list) -> list:
    num = len(list)
    for i in range(num):
        swapped = False
        for j in range(num-i-1):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
                swapped = True

        if not swapped:
            break
    return list

my_list = [3, 5, 2, 4, 6, 7, 9, 8, 1]
print(my_list)
print(bubble_sort(my_list))