function action(argument) {
  // simple case
  return argument;
}

function calculate(key, value) {
  var value_combined = [key, value];
  var value_chained = key + value;
  var value_result = key * value_chained;
  var value_action = action(value_result) + key;

  // jumping between matches
  return value_combined;
}

function execute(arg1, arg2) {
  // parenthesis completion
  return calculate(arg1, arg2);
}

// line completion
action(value_result) + key;