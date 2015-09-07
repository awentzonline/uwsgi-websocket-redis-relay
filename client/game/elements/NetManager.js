'use strict';

var _ = require('underscore');

function NetManager(options) {
  options = options || {};
  options.protocol = options.protocol || 'ws';
  options.host = options.host || document.location.hostname;
  options.port = options.port || document.location.port;
  options.path = options.path || document.location.pathname;

  this.handlers = {};

  var url = options.protocol + '://' + options.host;
  if (options.port) {
    url += ':' + options.port;
  }
  url += options.path;
  var socket = this.socket = new WebSocket(url);
  socket.onopen = this.onOpen.bind(this);
  socket.onmessage = this.onMessage.bind(this);
  socket.onerror = this.onError.bind(this);
}

NetManager.prototype.onOpen = function () {
  console.log('connected')
};

NetManager.prototype.onMessage = function (event) {
  var data = JSON.parse(event.data);
  var kind = data[0];
  data = data[1];
  //console.log([kind, data]);
  var handlers = this.handlers[kind];
  if (handlers) {
    _.each(handlers, function (v) {
      v(data);
    });
  }
};

NetManager.prototype.onError = function (event) {
  console.log('error');
  console.log(event);
};

NetManager.prototype.sendMessage = function (kind, data) {
  this.socket.send(JSON.stringify([kind, data]));
};

NetManager.prototype.registerMessageHandler = function (kind, handler) {
  if (!this.handlers[kind]) {
    this.handlers[kind] = [];
  }
  this.handlers[kind].push(handler);
};

module.exports = NetManager;
