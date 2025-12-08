use std::collections::HashSet;
use std::collections::VecDeque;
use std::time::Instant;

const INPUT: &str = include_str!("input.txt");

fn parse_input() -> Vec<Vec<char>> {
    INPUT
        .trim()
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}

fn part1(input: &Vec<Vec<char>>) -> usize {
    let rows = input.len();
    let cols = input[0].len();
    let mut accessible = 0;

    for i in 0..rows {
        for j in 0..cols {
            if input[i][j] != '@' {
                continue;
            }

            let mut count = 0u16;
            for di in -1isize..=1 {
                for dj in -1isize..=1 {
                    if di == 0 && dj == 0 {
                        continue;
                    }

                    let ni = i as isize + di;
                    let nj = j as isize + dj;
                    if ni >= 0
                        && ni < rows as isize
                        && nj >= 0
                        && nj < cols as isize
                        && input[ni as usize][nj as usize] == '@'
                    {
                        count += 1
                    }
                }
            }

            if count < 4 {
                accessible += 1;
            }
        }
    }
    accessible
}

fn part2(input: &Vec<Vec<char>>) -> usize {
    let rows = input.len();
    let cols = input[0].len();
    let mut occupied = HashSet::new();

    for i in 0..rows {
        for j in 0..cols {
            if input[i][j] == '@' {
                occupied.insert((i as isize, j as isize));
            }
        }
    }

    let initial_size = occupied.len();

    let neighbours = |i: isize, j: isize| {
        (-1isize..=1).flat_map(move |di| {
            (-1isize..=1).filter_map(move |dj| {
                if di == 0 && dj == 0 {
                    None
                } else {
                    Some((i + di, j + dj))
                }
            })
        })
    };

    let count_neighbours = |pos: &(isize, isize), occupied: &HashSet<(isize, isize)>| {
        neighbours(pos.0, pos.1)
            .filter(|n| occupied.contains(n))
            .count()
    };

    let mut q: VecDeque<(isize, isize)> = occupied
        .iter()
        .filter(|pos| count_neighbours(pos, &occupied) < 4)
        .copied()
        .collect();

    while let Some(pos) = q.pop_front() {
        if !occupied.remove(&pos) {
            continue;
        }

        for n in neighbours(pos.0, pos.1) {
            if occupied.contains(&n) && count_neighbours(&n, &occupied) < 4 {
                q.push_back(n);
            }
        }
    }

    initial_size - occupied.len()
}

fn main() {
    let t = Instant::now();
    let input = parse_input();
    println!("parse_input: - ({:?})", t.elapsed());

    let t = Instant::now();
    let a1 = part1(&input);
    println!("part1: {} ({:?})", a1, t.elapsed());

    let t = Instant::now();
    let a2 = part2(&input);
    println!("part2: {} ({:?})", a2, t.elapsed());
}
