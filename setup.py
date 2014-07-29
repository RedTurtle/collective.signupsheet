from setuptools import setup, find_packages
import os

version = '0.1.1'

tests_require = ['plone.app.testing', ]

setup(name='collective.signupsheet',
      version=version,
      description="A Plone solution for manage signup attendance to events",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='signupsheet plone plonegov ploneformgen event subscription',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/collective.signupsheet',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'Products.PloneFormGen',
          'uwosh.pfg.d2c>=2.3.0b4'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
