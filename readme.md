# HMM Implementation on S&P 500 Stock Data

This repository contains an implementation of Hidden Markov Models (HMMs) on S&P 500 stock data. The HMM is used for modeling the stock prices and making predictions.

## Forward-Backward Algorithm

The Forward-Backward algorithm is used for computing the posterior probabilities of the hidden states given the observations.

### Forward Step
The forward probability \(\alpha_t(i)\) is the probability of being in state \(i\) at time \(t\) and having observed the sequence \(O_1, O_2, ..., O_t\).

\[
\alpha_t(i) = P(O_1, O_2, ..., O_t, X_t = S_i | \lambda)
\]

### Backward Step
The backward probability \(\beta_t(i)\) is the probability of the ending partial sequence from \(t+1\) to \(T\), given the state \(i\) at time \(t\).

\[
\beta_t(i) = P(O_{t+1}, O_{t+2}, ..., O_T | X_t = S_i, \lambda)
\]

## Viterbi Algorithm

The Viterbi algorithm is used for finding the most likely sequence of hidden states.

### Induction Step
The induction step updates the highest probability of any path that reaches each state \(i\) at time \(t\), which includes state \(j\) at time \(t-1\).

\[
\delta_t(i) = \max_{j} \left[ \delta_{t-1}(j) \cdot a_{ji} \right] \cdot b_i(O_t)
\]

\[
\psi_t(i) = \arg\max_{j} \left[ \delta_{t-1}(j) \cdot a_{ji} \right]
\]

## Baum-Welch Algorithm

The Baum-Welch algorithm is an Expectation-Maximization (EM) algorithm used for finding the unknown parameters of the HMM.

### Expectation Step
Calculate the expected number of transitions from state \(i\) to state \(j\) and the expected number of times in state \(i\).

\[
\xi_t(i, j) = \frac{\alpha_t(i) \cdot a_{ij} \cdot b_j(O_{t+1}) \cdot \beta_{t+1}(j)}{\sum_{i=1}^N \sum_{j=1}^N \alpha_t(i) \cdot a_{ij} \cdot b_j(O_{t+1}) \cdot \beta_{t+1}(j)}
\]

\[
\gamma_t(i) = \frac{\alpha_t(i) \cdot \beta_t(i)}{\sum_{i=1}^N \alpha_t(i) \cdot \beta_t(i)}
\]

### Maximization Step
Re-estimate the parameters of the HMM.

\[
\hat{a}_{ij} = \frac{\sum_{t=1}^{T-1} \xi_t(i, j)}{\sum_{t=1}^{T-1} \gamma_t(i)}
\]

\[
\hat{b}_j(k) = \frac{\sum_{t=1, O_t = k}^{T} \gamma_t(j)}{\sum_{t=1}^{T} \gamma_t(j)}
\]

\[
\hat{\pi}_i = \gamma_1(i)
\]

## Usage

To use this repository, clone it and follow the instructions in the provided notebooks and scripts. Ensure you have the required dependencies installed.

```bash
git clone https://github.com/amnry/daily-stocks-HMM-predict
