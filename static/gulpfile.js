var gulp = require('gulp'),
	browserify = require('browserify'),
	source = require('vinyl-source-stream'),
	gulpReact = require('gulp-react'),
	runSequence = require('run-sequence'),
	babel = require('gulp-babel'),
	stylus = require('gulp-stylus');


gulp.task('stylus', function() {
	gulp.src('./dev/styl/*.styl')
		.pipe(stylus())
		.pipe(gulp.dest('./ready/css/'));
});

gulp.task('compile-jsx', function() {
	gulp.src('./dev/js/*.jsx')
		.pipe(gulpReact())
		.pipe(babel())
		.pipe(gulp.dest('./ready/js/'))
});

gulp.task('babel', function() {
	gulp.src('./dev/js/*.js')
		.pipe(babel())
		.pipe(gulp.dest('./ready/js/'));
});

gulp.task('browserify', function () {
	return browserify('./ready/js/app.js')
		.bundle()
		.pipe(source('final.js'))
		.pipe(gulp.dest('./ready/js/'));
});

gulp.task('general', function() {
	runSequence(
		'compile-jsx',
		'babel',
		'browserify'
	);
});

gulp.task('default', function() {
	gulp.watch('./dev/styl/*', ['stylus']);
	gulp.watch('./dev/js/*', ['general']);
});
