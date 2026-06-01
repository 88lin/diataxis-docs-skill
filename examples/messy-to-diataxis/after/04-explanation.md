# Explanation: why QuokkaDB chose an LSM-tree engine

> Diataxis form: **Explanation** (cognition + acquisition). The reader wants to understand the why.

## Origin

QuokkaDB started as a side project at a small infrastructure team. The team had been burned by overly complex distributed databases that hid their behavior behind query planners and consensus protocols. The original design goals were:

- fit in a single binary
- be predictable under load
- make transactions boring
- support ACID on a single node

## Why single-node first

Most of the team's workloads were either local caches for CLI tools, embedded stores for desktop apps, or a prototyping store before graduating to a larger system. None of them needed multi-node consensus. The team deliberately chose to optimize for the single-node case and accept that scaling out would be a future problem.

## Why ACID

The team's customers had been bitten by eventually-consistent stores that lost recent writes during node failures. ACID was non-negotiable, even if it cost some throughput. The team decided that **predictable correctness** was worth more than peak performance for their users.

## Why an LSM-tree

The dominant storage engines in the team's reference set were B-trees and LSM-trees. Both are mature. The choice was driven by workload shape.

- The team's write-heavy workloads dominate the read path.
- LSM-trees convert random writes into sequential writes, which is friendly to spinning disks and to most SSDs.
- LSM-trees also keep recent writes in memory and flush in batches, which fits the team's "many small writes" pattern.

The tradeoff is that **range scans are slower** than they would be on a B-tree store, because the engine may need to merge several sorted runs. For point reads, both engines are similar.

## What we left out

The team considered but rejected several features in v1:

- **Multi-node replication.** Adding it would have delayed v1 by a year and forced the team to revisit the consistency story. They chose to ship single-node first and treat replication as a v2 problem.
- **A query language.** The team wanted key-value semantics and a small API surface. SQL would have invited feature creep.
- **Pluggable storage engines.** Two engines is already a maintenance burden. One engine, well understood, beats two engines half-understood.

## Implications for users

If your workload is point reads and point writes on a single node, QuokkaDB is in its sweet spot. If you need fast range scans across many rows, or if you need cross-node consistency, you should look elsewhere and accept the additional operational complexity.

## Related reading

- The [tutorial](01-tutorial.md) shows the engine in action.
- The [how-to guide](02-how-to.md) shows how to configure it for common workloads.
- The [reference](03-reference.md) lists the exact options and limits.
