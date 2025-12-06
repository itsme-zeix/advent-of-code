use rayon::prelude::*;
use std::{thread::available_parallelism, thread::scope, time::Instant};

/*
parse_input:                    30.125µs
day01:                          9.602042ms
day02 (sequential):             40.613083ms
day02 (parallel, std::threads): 11.805708ms
day02 (parallel, rayon):        7.765291ms
*/

const INPUT: &str = include_str!("input.txt");

fn parse_input() -> Vec<(u64, u64)> {
    INPUT
        .trim()
        .split(',')
        .map(|s| {
            let (a, b) = s.split_once('-').expect("invalid input");
            (
                a.parse::<u64>().expect("not a valid int"),
                b.parse::<u64>().expect("not a valid int"),
            )
        })
        .collect()
}

fn count_digits(n: u64) -> u32 {
    if n == 0 {
        return 1;
    }
    n.checked_ilog10().unwrap_or(0) + 1
}

fn get_first_n_digits(num: u64, num_digits: u32, digits: u32) -> u64 {
    let divisions = num_digits - digits;
    let power_of_ten = 10u64.pow(divisions);
    num / power_of_ten
}

fn is_invalid(id: u64, candidate: u64, id_len: u32, candidate_len: u32) -> bool {
    let repeat_count = id_len / candidate_len;
    let mut repeated = 0;
    let pow10 = 10u64.pow(candidate_len);

    for _ in 0..repeat_count {
        repeated = repeated * pow10 + candidate;
    }
    id == repeated
}

fn part1(input: &[(u64, u64)]) -> u64 {
    let mut res: u64 = 0;

    for &(l, r) in input {
        for id_int in l..=r {
            let id_len = count_digits(id_int);

            if id_len % 2 != 0 {
                continue;
            }

            let candidate_len = id_len / 2;
            if is_invalid(
                id_int,
                get_first_n_digits(id_int, id_len, candidate_len),
                id_len,
                candidate_len,
            ) {
                res += id_int;
            }
        }
    }
    res
}

fn part2(input: &[(u64, u64)]) -> u64 {
    let mut res: u64 = 0;

    for &(l, r) in input {
        for id_int in l..=r {
            let id_len = count_digits(id_int);
            let max_candidate_len = id_len / 2;

            for candidate_len in (1..=max_candidate_len).rev() {
                if id_len % candidate_len != 0 {
                    continue;
                }

                if is_invalid(
                    id_int,
                    get_first_n_digits(id_int, id_len, candidate_len),
                    id_len,
                    candidate_len,
                ) {
                    res += id_int;
                    break;
                }
            }
        }
    }
    res
}

fn part2_parallel_std(input: &[(u64, u64)]) -> u64 {
    let num_threads = available_parallelism().map(|x| x.get()).unwrap_or(1);

    // add num_threads - 1for ceiling division
    let chunk_size = (input.len() + num_threads - 1) / num_threads;

    scope(|s| {
        let handles: Vec<_> = input
            .chunks(chunk_size)
            .map(|chunk| {
                s.spawn(move || {
                    let mut local_sum = 0u64;
                    for &(l, r) in chunk {
                        for id_int in l..=r {
                            let id_len = count_digits(id_int);
                            let max_candidate_len = id_len / 2;
                            for candidate_len in (1..=max_candidate_len).rev() {
                                if id_len % candidate_len != 0 {
                                    continue;
                                }
                                if is_invalid(
                                    id_int,
                                    get_first_n_digits(id_int, id_len, candidate_len),
                                    id_len,
                                    candidate_len,
                                ) {
                                    local_sum += id_int;
                                    break;
                                }
                            }
                        }
                    }
                    local_sum
                })
            })
            .collect();

        handles.into_iter().map(|x| x.join().unwrap()).sum()
    })
}

fn part2_parallel_rayon(input: &[(u64, u64)]) -> u64 {
    input
        .par_iter()
        .map(|&(l, r)| {
            let mut local_sum = 0u64;
            for id_int in l..=r {
                let id_len = count_digits(id_int);
                let max_candidate_len = id_len / 2;

                for candidate_len in (1..=max_candidate_len).rev() {
                    if id_len % candidate_len != 0 {
                        continue;
                    }

                    if is_invalid(
                        id_int,
                        get_first_n_digits(id_int, id_len, candidate_len),
                        id_len,
                        candidate_len,
                    ) {
                        local_sum += id_int;
                        break;
                    }
                }
            }
            local_sum
        })
        .sum()
}

fn main() {
    let t = Instant::now();
    let input = parse_input();
    println!("parse_input: - ({:?})", t.elapsed());

    let t = Instant::now();
    let a1 = part1(&input);
    println!("day01: {} ({:?})", a1, t.elapsed());

    let t = Instant::now();
    let a2 = part2(&input);
    println!("day02: {} ({:?})", a2, t.elapsed());

    let t = Instant::now();
    let a2 = part2_parallel_std(&input);
    println!("day02_parallel_std: {} ({:?})", a2, t.elapsed());

    let t = Instant::now();
    let a2 = part2_parallel_rayon(&input);
    println!("day02_parallel_rayon: {} ({:?})", a2, t.elapsed());
}
