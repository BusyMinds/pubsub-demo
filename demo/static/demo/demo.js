'use strict';

function DemoCtrl($http) {

    var vm = this;

    vm.pushing = false;
    vm.pulling = false;
    vm.pushes = [];
    vm.pulls = [];

    function onPushSuccess() {
        vm.pushing = false;
        vm.pushes.push(vm.data);
        vm.data = null;
    }

    vm.push = function(data) {
        vm.pushing = true;
        $http.post('/api/', {data: vm.data}).then(onPushSuccess);
    };

    function onPullSuccess(res) {
        vm.pulling = false;
        vm.pulls.push(res.data.message);
    }

    vm.pull = function() {
        vm.pulling = true;
        $http.get('/api/').then(onPullSuccess);
    };
}

angular.module('PubSubDemo', [])
    .controller('DemoCtrl', DemoCtrl);

DemoCtrl.$inject = ['$http'];
