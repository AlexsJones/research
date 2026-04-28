# When Less Latent Leads to Better Relay: Information-Preserving Compression for Latent Multi-Agent LLM Collaboration

## Summary
- Orthogonal Backfill injects low-rank residual from discarded states into retained states
- 79.8%-89.4% communication cost reduction vs full KV relay
- Achieves best results on 7 of 9 benchmarks
- More information does not lead to better communication -- quality matters more

## Relevance to Membrane
Directly validates Layer 1 permeability argument. Shows preserving the most useful information matters more than preserving everything. Reduces communication cost by 79.8%-89.4% while maintaining performance.

## Citations
- arXiv: https://arxiv.org/abs/2604.13349
