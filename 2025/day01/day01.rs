use std::fs;
use std::time::Instant;

fn read_input(path: &str) -> Vec<(char, i16)> {
    let input = fs::read_to_string(path)
        .expect("failed to read input file");

    input.lines()
        .map(|s| {
            let (a, b) = s.split_at(1);
            let dir = a.chars().next().expect("empty line");
            let dist = b.trim().parse::<i16>().expect("invalid number");
            (dir, dist)
        })
        .collect()
}

fn day01(input: &[(char, i16)]) -> i16 {
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

fn day02(input: &[(char, i16)]) -> i16 {
    let mut state: i16 = 50;
    let mut res: i16 = 0;

    for (dir, mut dist) in input {
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
    let input = read_input("input.txt");
    println!("read_input ({:?})", t.elapsed());

    let t = Instant::now();
    let a1 = day01(&input);
    println!("day01: {} ({:?})", a1, t.elapsed());

    let t = Instant::now();
    let a2 = day02(&input);
    println!("day02: {} ({:?})", a2, t.elapsed());
}
