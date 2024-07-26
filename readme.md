# HMM Implementation on S&P 500 Stock Data

This repository contains an implementation of Hidden Markov Models (HMMs) on S&P 500 stock data. The HMM is used for modeling the stock prices and making predictions.

## Forward-Backward Algorithm

The Forward-Backward algorithm is used for computing the posterior probabilities of the hidden states given the observations.

### Forward Step
The forward probability \(\alpha_t(i)\) is the probability of being in state \(i\) at time \(t\) and having observed the sequence \(O_1, O_2, ..., O_t\).

![Forward Step Formula](https://latex.codecogs.com/svg.latex?\alpha_t(i)%20=%20P(O_1,%20O_2,%20...,%20O_t,%20X_t%20=%20S_i%20|%20\lambda))

### Backward Step
The backward probability \(\beta_t(i)\) is the probability of the ending partial sequence from \(t+1\) to \(T\), given the state \(i\) at time \(t\).

![Backward Step Formula](https://latex.codecogs.com/svg.latex?\beta_t(i)%20=%20P(O_{t+1},%20O_{t+2},%20...,%20O_T%20|%20X_t%20=%20S_i,%20\lambda))

## Viterbi Algorithm

The Viterbi algorithm is used for finding the most likely sequence of hidden states.

### Induction Step
The induction step updates the highest probability of any path that reaches each state \(i\) at time \(t\), which includes state \(j\) at time \(t-1\).

![Induction Step Formula 1](https://latex.codecogs.com/svg.latex?\delta_t(i)%20=%20\max_{j}%20\left[%20\delta_{t-1}(j)%20\cdot%20a_{ji}%20\right]%20\cdot%20b_i(O_t))

![Induction Step Formula 2](https://latex.codecogs.com/svg.latex?\psi_t(i)%20=%20\arg\max_{j}%20\left[%20\delta_{t-1}(j)%20\cdot%20a_{ji}%20\right])

## Baum-Welch Algorithm

The Baum-Welch algorithm is an Expectation-Maximization (EM) algorithm used for finding the unknown parameters of the HMM.

### Expectation Step
Calculate the expected number of transitions from state \(i\) to state \(j\) and the expected number of times in state \(i\).

![Expectation Step Formula 1](https://latex.codecogs.com/svg.latex?\xi_t(i,%20j)%20=%20\frac{\alpha_t(i)%20\cdot%20a_{ij}%20\cdot%20b_j(O_{t+1})%20\cdot%20\beta_{t+1}(j)}{\sum_{i=1}^N%20\sum_{j=1}^N%20\alpha_t(i)%20\cdot%20a_{ij}%20\cdot%20b_j(O_{t+1})%20\cdot%20\beta_{t+1}(j)})

![Expectation Step Formula 2](https://latex.codecogs.com/svg.latex?\gamma_t(i)%20=%20\frac{\alpha_t(i)%20\cdot%20\beta_t(i)}{\sum_{i=1}%20^N%20\alpha_t(i)%20\cdot%20\beta_t(i)})

### Maximization Step
Re-estimate the parameters of the HMM.

![Maximization Step Formula 1](https://latex.codecogs.com/svg.latex?\hat{a}_{ij}%20=%20\frac{\sum_{t=1}^{T-1}%20\xi_t(i,%20j)}{\sum_{t=1}^{T-1}%20\gamma_t(i)})

![Maximization Step Formula 2](https://latex.codecogs.com/svg.latex?\hat{b}_j(k)%20=%20\frac{\sum_{t=1,%20O_t%20=%20k}^{T}%20\gamma_t(j)}{\sum_{t=1}^{T}%20\gamma_t(j)})

![Maximization Step Formula 3](https://latex.codecogs.com/svg.latex?\hat{\pi}_i%20=%20\gamma_1(i))

## Usage

To use this repository, clone it and follow the instructions in the provided notebooks and scripts. Ensure you have the required dependencies installed.

```bash
git clone https://github.com/yourusername/hmm-snp500.git
