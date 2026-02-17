import sys
import math


def calculate_freq_vector(text, lower_bound, upper_bound):
    vec = [[0]*26 for a in range(upper_bound)]
    for x in range(lower_bound, upper_bound):
        for i in range(0, len(text), x):
            if text[i].isalpha():
                index = ord(text[i]) - ord('a')
                vec[x][index] += 1
    print(vec)
    return vec

def compute_std(vec, lower_bound, upper_bound):
    stds = [0] * upper_bound
    square_sum = [0] * upper_bound
    square_sum[0] = vec[0] * vec[0]
    sumx = [0] * upper_bound
    sumx[0] = vec[0]
    for t in range(1, upper_bound):
        square_sum[t] = square_sum[t - 1] + vec[t] * vec [t]
        sumx[t] = sumx[t - 1] + vec[t]
        print(t)
    for i in range(lower_bound - 1, upper_bound, 1):
        stds[i] = math.sqrt(square_sum[i]/26 - sqr(sumx[i]/26))
        print(f"The sum of {i + 1} std. devs: {stds[i]}")

def sqr(x):
    y = x*x
    return y
            
if __name__ == "__main__":
    lower_bound = int(input())
    upper_bound = int(input())
    text = sys.stdin.read()
    text = list(text.lower())
    freq_vec = calculate_freq_vector(text, lower_bound, upper_bound)
    #compute_std(freq_vec, lower_bound, upper_bound)