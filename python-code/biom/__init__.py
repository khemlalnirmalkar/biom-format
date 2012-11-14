#!/usr/bin/env python

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2012, BIOM-Format Project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Greg Caporaso", 
               "Jose Clemente", "Justin Kuczynski"]
__license__ = "GPL"
__url__ = "http://biom-format.org"
__version__ = "1.0.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "daniel.mcdonald@colorado.edu"

__all__ = ['table','parse','csmat','sparsemat','sparsedict','util','unittest',
           'exception']

from sys import modules

from biom.exception import InvalidSparseBackendException
from biom.util import load_biom_config

biom_config = load_biom_config()

def set_sparse_backend(sparse_backend, warn=True):
    """Sets the sparse matrix backend to use in biom.table.

    Use this function to programmatically override the backend specified in the
    biom config file. Similar to matplotlib.use(). Has no effect if biom.table
    has already been imported.

    Arguments:
        sparse_backend - sparse backend string identifier
        warn - if True, will print out a warning if biom.table has already been
        loaded.
    """
    if 'biom.table' in modules:
        if warn:
            print ("Warning: biom.table has already been loaded. This call to "
                   "biom.set_sparse_backend() has no effect. It must be "
                   "called before biom.table is imported for the first time.")
    else:
        biom_config['python_code_sparse_backend'] = sparse_backend

def get_sparse_backend():
    """Returns the constructor and functions needed to use the current backend.

    Will look at whatever the current backend is in the loaded biom config
    dict. If one isn't specified, will default to SparseDict (this one should
    always work, regardless of the user's configuration). Will raise a
    ValueError if the current sparse backend isn't supported or cannot be used
    for whatever reason.
    """
    backend = biom_config['python_code_sparse_backend']
    if backend is None:
        backend = 'SparseDict'

    valid_backend = True
    if backend == 'CSMat':
        try:
            from biom.csmat import CSMat, to_csmat, dict_to_csmat, \
                list_dict_to_csmat, list_nparray_to_csmat, nparray_to_csmat, \
                list_list_to_csmat
            SparseObj = CSMat
            to_sparse = to_csmat
            dict_to_sparseobj = dict_to_csmat
            list_dict_to_sparseobj = list_dict_to_csmat
            list_nparray_to_sparseobj = list_nparray_to_csmat
            nparray_to_sparseobj = nparray_to_csmat
            list_list_to_sparseobj = list_list_to_csmat
        except ImportError:
            valid_backend = False
    elif backend == 'SparseMat':
        try:
            from biom.sparsemat import SparseMat, to_sparsemat, \
                dict_to_sparsemat, list_dict_to_sparsemat, \
                list_nparray_to_sparsemat, nparray_to_sparsemat, \
                list_list_to_sparsemat
            SparseObj = SparseMat
            to_sparse = to_sparsemat
            dict_to_sparseobj = dict_to_sparsemat
            list_dict_to_sparseobj = list_dict_to_sparsemat
            list_nparray_to_sparseobj = list_nparray_to_sparsemat
            nparray_to_sparseobj = nparray_to_sparsemat
            list_list_to_sparseobj = list_list_to_sparsemat
        except ImportError:
            valid_backend = False
    elif backend == 'SparseDict':
        try:
            from biom.sparsedict import SparseDict, to_sparsedict, \
                dict_to_sparsedict, list_dict_to_sparsedict, \
                list_nparray_to_sparsedict, nparray_to_sparsedict, \
                list_list_to_sparsedict
            SparseObj = SparseDict
            to_sparse = to_sparsedict
            dict_to_sparseobj = dict_to_sparsedict
            list_dict_to_sparseobj = list_dict_to_sparsedict
            list_nparray_to_sparseobj = list_nparray_to_sparsedict
            nparray_to_sparseobj = nparray_to_sparsedict
            list_list_to_sparseobj = list_list_to_sparsedict
        except ImportError:
            valid_backend = False
    else:
        valid_backend = False

    if not valid_backend:
        raise InvalidSparseBackendException("The sparse matrix backend '%s' "
                "could not be loaded because it is either unrecognized or "
                "your biom-format install does not support it (e.g. no "
                "Cython, so no access to SparseMat)." % backend)

    return SparseObj, to_sparse, dict_to_sparseobj, list_dict_to_sparseobj, \
           list_nparray_to_sparseobj, nparray_to_sparseobj, \
           list_list_to_sparseobj
