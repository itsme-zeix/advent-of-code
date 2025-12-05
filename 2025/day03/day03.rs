use std::time::Instant;

const INPUT: &str = include_str!("input.txt");

fn parse_input() -> Vec<String> {
    INPUT.trim().lines().map(|s| s.to_string()).collect()
}

fn solve(input: &[String], substr_length: usize) -> i128 {
    let mut res = 0;
    for line in input {
        let mut leftover_chars = line.len();
        let mut stack: Vec<char> = vec![];

        for ch in line.chars() {
            while leftover_chars > substr_length && stack.last().is_some_and(|&last| last < ch) {
                stack.pop();
                leftover_chars -= 1;
            }
            stack.push(ch);
        }

        let curr: String = stack.iter().take(substr_length).collect();
        res += curr.parse::<i128>().expect("Failed to parse string to int");
    }
    res
}

fn main() {
    let t = Instant::now();
    let input = parse_input();
    println!("parse_input: - ({:?})", t.elapsed());

    let t = Instant::now();
    let a1 = solve(&input, 2);
    println!("part1: {} ({:?})", a1, t.elapsed());

    let t = Instant::now();
    let a2 = solve(&input, 12);
    println!("part2: {} ({:?})", a2, t.elapsed());
}
