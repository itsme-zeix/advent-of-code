use std::time::Instant;

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
}
