clean:
	# cleaning
	@rm -rf ${BUILDDIR} dist *.egg-info .coverage .pytest MEDIA_ROOT MANIFEST .cache *.egg build STATIC
	@find . -name __pycache__ -prune | xargs rm -rf
	@find . -name "*.py?" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml
