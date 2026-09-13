# Labs

My personal playground for learning.

Whenever I pick up something new, a language, a framework, a tool, a concept, I create a directory for it here and practice inside it. Notes, snippets, small experiments, half-finished ideas: everything lives in one place so I can come back and look it up later instead of hunting through scattered folders and bookmarks.

This is a scratchpad, not a portfolio. Code here is written to understand something, not to ship it.

## Structure

One top-level directory per topic. Inside it, whatever structure makes sense for that topic.

```
labs/
├── js/          # JavaScript experiments and notes
├── python/      # Python experiments and notes
├── rust/        # Rust experiments and notes
├── shopify/     # Shopify / Liquid theme experiments
└── sql/         # SQL queries and database notes
```

| Directory               | What's in it                                                 |
| ----------------------- | ------------------------------------------------------------ |
| [`js/`](./js)           | JavaScript language features, patterns, and browser APIs     |
| [`python/`](./python)   | Python syntax, standard library, and scripting practice      |
| [`rust/`](./rust)       | Rust fundamentals: ownership, borrowing, and the type system |
| [`shopify/`](./shopify) | Shopify theme development and Liquid templating              |
| [`sql/`](./sql)         | SQL queries, joins, indexing, and schema design              |

## Conventions

A few rules I try to stick to, so this stays useful six months from now:

- **One topic per top-level directory.** If a topic gets big enough, split it into subdirectories by subtopic.
- **Every directory gets its own `README.md`** with what I was learning, where I learned it from, and anything that tripped me up.
- **Keep the "why" with the code.** A comment explaining why something works is worth more than the working code by itself.
- **Don't delete the broken attempts.** The thing that didn't work is often the more useful note.
- **Small and runnable.** Each experiment should stand on its own and run without much setup.

## Running things

Each directory has its own setup, since the stacks are different. Check the README inside the directory. In general:

```bash
# JavaScript
cd js && node <file>.js

# Python
cd python && python <file>.py

# Rust
cd rust/<project> && cargo run

# SQL
# Run the .sql files against a local database
```

## Adding a new topic

```bash
mkdir <topic>
cd <topic>
touch README.md
```

Then note down what I'm learning and why, and start experimenting.

## A note for visitors

If you found this repo, you're welcome to look around, but the code is written for me. It's rough, it's inconsistent, and some of it is wrong on purpose because that's how I was thinking about the problem at the time.
