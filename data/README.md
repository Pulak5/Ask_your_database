# Data Sources and Licenses

## Demo Database: Pagila (PostgreSQL Flavour)
- **Source:** [https://github.com/devrimgunduz/pagila](https://github.com/devrimgunduz/pagila) and [PostgreSQL Sample Databases](https://github.com/postgresql/samples)
- **License:** PostgreSQL License (Permissive, BSD-like)
- **Description:** A DVD rental store business database covering inventory, rentals, film metadata, actors, categories, and customer payments.
- **Flavour:** PostgreSQL 16+ compliant DDL with standard `IDENTITY` primary keys and foreign key constraints.

### Tables Included
| Table | Rows (Seed) | Description |
|---|---|---|
| `country` | 10 | Lookup table for customer and store countries |
| `city` | 20 | Cities linked to countries |
| `address` | 30 | Physical addresses for customers, staff, and stores |
| `language` | 5 | Spoken languages for films |
| `category` | 16 | Film genres (Action, Comedy, Sci-Fi, Drama, etc.) |
| `film` | 50 | Film catalog: rental rates, replacement costs, ratings, lengths |
| `film_category` | 65 | Many-to-many junction between films and categories |
| `actor` | 30 | Film actors |
| `film_actor` | 110 | Many-to-many junction between films and actors |
| `store` | 2 | Physical retail rental store locations |
| `staff` | 2 | Store managers and cashiers |
| `customer` | 30 | Registered store customers |
| `inventory` | 100 | Physical copies of films present in specific stores |
| `rental` | 200 | Rental transactions tracking checkout and return dates |
| `payment` | 180 | Monetary transactions linked to customers and rentals |

## Evaluation Dataset (`data/eval/demo_eval.jsonl`)
- **Size:** 100 rigorously constructed, held-out question/SQL pairs.
- **Difficulty distribution:** 20 Easy, 30 Medium, 30 Hard, 20 Edge/Unanswerable.
- **Isolation Policy:** Held-out test set; strictly segregated from any training corpus.
- **Validation:** Every answerable gold query executes against the demo database and returns verified non-empty result sets.

## Training Dataset (`data/train/`)
- **Generation:** Synthesized via `src/training/prepare_data.py`.
- **Sources:** Spider dataset (train split, filtered for PostgreSQL compatibility) and synthetic domain-specific pairs.
- **Leakage Guard:** Automated exact and fuzzy string similarity deduplication against `data/eval/demo_eval.jsonl` (SequenceMatcher > 0.8 threshold).

