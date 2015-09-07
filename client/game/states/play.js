'use strict';

var _ = require('underscore');
var NetManager = require('../elements/NetManager.js');

function Play() {};

Play.prototype = {
  create: function() {
    // Don't stop simulating when we leave the window. This is so
    // you can see the movement from another browser window locally.
    this.stage.disableVisibilityChange = true

    this.netManager = new NetManager({
      port: 9000
    });
    this.netSprites = {};
    this.netManager.registerMessageHandler('zthings', this.updateNetSprites.bind(this));
    this.game.physics.startSystem(Phaser.Physics.ARCADE);
  },
  updateNetSprites: function (data) {
    _.each(data, function (netData) {
      if (!this.netSprites[netData.id]) {
        var sprite = this.netSprites[netData.id] = this.game.add.sprite(
          netData.x, netData.y, netData.sprite
        );
        sprite.inputEnabled = true;
        sprite.input.enableDrag();
        sprite.events.onDragStart.add(this.onDragStart, this);
        sprite.events.onDragStop.add(this.onDragStop, this);
        sprite._thingId = netData.id;
      } else {
        var sprite = this.netSprites[netData.id];
        if (sprite.x != netData.x || sprite.y != netData.y) {
          this.game.add.tween(sprite).to({
            x: netData.x,
            y: netData.y
          }, 250, Phaser.Easing.Quartic.In, true);
        }
        sprite.key = netData.sprite;
      }
    }, this)
  },
  onDragStart: function (sprite, pointer) {

  },
  onDragStop: function (sprite, pointer) {
    var thingId = sprite._thingId;
    this.netManager.sendMessage('tup', [thingId, {
      x: sprite.x,
      y: sprite.y
    }]);
  },
  update: function() {

  }
};

module.exports = Play;
