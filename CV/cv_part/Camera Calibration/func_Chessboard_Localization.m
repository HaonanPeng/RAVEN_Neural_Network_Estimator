   function [location,rotationMatrix] = func_Chessboard_Localization(I,cameraParams,squareSize)
        [imagePoints,boardSize,imagesUsed] = detectCheckerboardPoints(I);
        figure()
        imshow(I);
        hold on;
        plot(imagePoints(:,1),imagePoints(:,2),'ro','LineWidth',2);
        plot(imagePoints(1,1),imagePoints(1,2),'yo','LineWidth',2);
        worldPoints = generateCheckerboardPoints(boardSize, squareSize);
        [rotationMatrix,translationVector] = extrinsics(imagePoints,worldPoints,cameraParams);
        [orientation,location] = extrinsicsToCameraPose(rotationMatrix,translationVector);
    end