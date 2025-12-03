use std::time::Instant;

const INPUT: &str = include_str!("input.txt");

fn parse_input() -> Vec<(char, i16)> {
    INPUT.lines()
        .map(|s| {
            let (a, b) = s.split_at(1);
            let dir = a.chars().next().expect("empty line");
            let dist = b.trim().parse::<i16>().expect("invalid number");
            (dir, dist)
        })
        .collect()
}

fn part1(input: &[(char, i16)]) -> i16 {
    let mut state: i16 = 50;
    let mut res: i16 = 0;

    for (dir, dist) in input {
        match dir {
            'L' => {
                state = (state - dist).rem_euclid(100);
            }
            'R' => {
                state = (state + dist).rem_euclid(100);
            }
            _ => panic!("Invalid direction {}", dir),
        }
        if state == 0 {
            res += 1;
        }
    }
    res
}

fn part2(input: &[(char, i16)]) -> i16 {
    let mut state: i16 = 50;
    let mut res: i16 = 0;

    for &(ref dir, mut dist) in input {
        let full_rotations = dist / 100;
        dist %= 100;
        res += full_rotations;

        match dir {
            'L' => {
                if state > 0 && dist >= state {
                    res += 1;
                }
                state = (state - dist).rem_euclid(100);
            }
            'R' => {
                if state > 0 && dist >= (100 - state) {
                    res += 1;
                }
                state = (state + dist).rem_euclid(100);
            }
            _ => panic!("Invalid direction {}", dir)
        }
    }
    res
}

fn main() {
    let t = Instant::now();
    let input = parse_input();
    println!("read_input ({:?})", t.elapsed());

    let t = Instant::now();
    let a1 = part1(&input);
    println!("day01: {} ({:?})", a1, t.elapsed());

    let t = Instant::now();
    let a2 = part2(&input);
    println!("day02: {} ({:?})", a2, t.elapsed());
}
