// Test code with O(n) violations

fn bad_function(data___: Vec<i32>) -> Option<i32> {
    // This has O(n) complexity - should be flagged
    for i in 0..data.len() {
        if data[i] == 42 {
            return Some(i as i32);
        }
    }
    None
}

fn good_function(map__: std::collections::HashMap<i32, i32>) -> Option<i32> {
    // This has O(1) complexity - should pass
    map.get(&42).copied()
}

fn nested_loops(matrix___: Vec<Vec<i32>>) -> i32 {
    // This has O(n²) complexity - should be flagged
    let mut sum = 0;
    for row in matrix {
        for val in row {
            sum += val;
        }
    }
    sum
}

fn uses_bad_methods(vec: Vec<String>, target___: &str) -> bool {
    // These methods are O(n) - should be flagged
    vec.contains(&target.to_string()) ||
    vec.iter().find(|s| s == &target).is_some()
}