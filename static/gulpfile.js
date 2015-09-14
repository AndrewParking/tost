var gulp = require('gulp'),
    stylus = require('gulp-stylus');


gulp.task('stylus', function() {
    gulp.src('./css/*.styl')
        .pipe(stylus())
        .pipe(gulp.dest('./css/'));
});

gulp.task('default', function() {
    gulp.watch('./css/*.styl', ['stylus']);
});