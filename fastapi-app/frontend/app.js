var app = angular.module("todoApp", []);

app.controller("TodoController", function($scope, $http) {
  const API = "http://127.0.0.1:8000/tasks";

  $scope.tasks = [];
  $scope.newTask = { title: "", completed: false };

  // Fetch all tasks
  $scope.getTasks = function() {
    $http.get(API).then(function(response) {
      $scope.tasks = response.data;
    });
  };

  // Add a task
  $scope.addTask = function() {
    if (!$scope.newTask.title.trim()) return;

    const taskToAdd = {
      id: 0,  // FastAPI assigns the real ID
      title: $scope.newTask.title,
      completed: false
    };

    $http.post(API, taskToAdd).then(function() {
      $scope.newTask.title = "";
      $scope.getTasks();
    });
  };

  // Update a task
  $scope.updateTask = function(task) {
    $http.put(`${API}/${task.id}`, task).then(function() {
      $scope.getTasks();
    });
  };

  // Delete a task
  $scope.deleteTask = function(taskId) {
    $http.delete(`${API}/${taskId}`).then(function() {
      $scope.getTasks();
    });
  };

  // Load tasks on startup
  $scope.getTasks();
});
