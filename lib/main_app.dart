// Copyright (c) 2015, <your name>. All rights reserved. Use of this source code
// is governed by a BSD-style license that can be found in the LICENSE file.
@HtmlImport('main_app.html')
library untitled.lib.main_app;

import 'dart:html';

import 'package:polymer_elements/paper_input.dart';
import 'package:polymer/polymer.dart';
import 'package:web_components/web_components.dart';
import 'package:stagexl/stagexl.dart';

/// Uses [PaperInput]
@PolymerRegister('main-app')
class MainApp extends PolymerElement {
  @property
  String text;

  Stage stage;
  RenderLoop renderLoop;
  ResourceManager resourceManager;

  /// Constructor used to create instance of MainApp.
  MainApp.created() : super.created();

  @reflectable
  String reverseText(String text) {
    return text.split('').reversed.join('');
  }

  attached() {
    super.attached();

    // configure StageXL default options

    StageXL.stageOptions.renderEngine = RenderEngine.WebGL;
    StageXL.stageOptions.stageScaleMode = StageScaleMode.SHOW_ALL;
    StageXL.stageOptions.stageAlign = StageAlign.NONE;
    StageXL.bitmapDataLoadOptions.webp = false;

    // init Stage and RenderLoop

    stage = new Stage(querySelector('#stage'), width: 1600, height: 600);
    renderLoop = new RenderLoop();
    renderLoop.addStage(stage);

    // load resources

    resourceManager = new ResourceManager()
      ..addTextureAtlas("ta1", "images/anim.json")
      ..addBitmapData("background", "images/background.png")
      ..load().then((result) => startAnimation());
  }

  void startAnimation() {
    Bitmap back = new Bitmap(resourceManager.getBitmapData("background"));

    stage.addChild(back);
    var scaling = 1;

    // Get all the "walk" bitmapDatas from the texture atlas.

    var textureAtlas = resourceManager.getTextureAtlas("ta1");
    var bitmapDatas = textureAtlas.getBitmapDatas("frame");

    // Create a flip book with the list of bitmapDatas.

    var rect = stage.contentRectangle;

    var frames = bitmapDatas.length;
    var flipBook = new FlipBook(bitmapDatas, frames)
      ..x = rect.center.x / 2
      ..y = rect.center.y
      ..scaleX = scaling
      ..scaleY = scaling
      ..addTo(stage)
      ..play();

    stage.juggler..add(flipBook);
  }

  void stopAnimation(FlipBook flipbook) {
    stage.removeChild(flipbook);
    stage.juggler.remove(flipbook);
  }

//  /// Called when an instance of main-app is removed from the DOM.
//  detached() {
//    super.detached();
//  }

//  /// Called when an attribute (such as a class) of an instance of
//  /// main-app is added, changed, or removed.
//  attributeChanged(String name, String oldValue, String newValue) {
//    super.attributeChanged(name, oldValue, newValue);
//  }

//  /// Called when main-app has been fully prepared (Shadow DOM created,
//  /// property observers set up, event listeners attached).
//  ready() {
//  }
}
