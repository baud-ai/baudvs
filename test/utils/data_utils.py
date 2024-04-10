# Copyright 2019 The Vearch Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

# -*- coding: UTF-8 -*-

import shutil
import tarfile
from ftplib import FTP
from urllib.parse import urlparse
import socket
import numpy as np
import os


__description__ = """ test data utils for vearch """


def get_ftp_ip(url):
    parsed_url = urlparse(url)
    ftp_host = parsed_url.hostname
    ip_address = socket.gethostbyname(ftp_host)

    return ip_address


def ivecs_read(fname):
    a = np.fromfile(fname, dtype="int32")
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()


def fvecs_read(fname):
    return ivecs_read(fname).view("float32")


def download_sift(logger, host, dirname, local_dir, filename):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    if os.path.isfile(local_dir + filename):
        logger.debug("%s exists, no need to download" % (local_dir + filename))
        return True
    ftp = FTP(host)
    ftp.login()
    ftp.set_pasv(True)
    ftp.cwd(dirname)

    with open(local_dir + filename, "wb") as local_file:
        ftp.retrbinary("RETR " + filename, local_file.write)
    ftp.quit()

    if os.path.isfile(local_dir + filename):
        logger.debug("%s successful download" % (local_dir + filename))
        return True
    else:
        logger.error("%s download failed" % (local_dir + filename))
        return False


def untar(logger, fname, dirs, untar_result_dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    if not os.path.isfile(dirs + fname):
        logger.debug("%s not exist, cann't untar" % (fname))
        return
    if os.path.exists(dirs + untar_result_dirs):
        logger.debug("%s exist, no need to untar" % (dirs + untar_result_dirs))
        return
    t = tarfile.open(dirs + fname)
    t.extractall(path=dirs)


def load_sift1M(logger):
    xt = fvecs_read("sift/sift_learn.fvecs")
    xb = fvecs_read("sift/sift_base.fvecs")
    xq = fvecs_read("sift/sift_query.fvecs")
    gt = ivecs_read("sift/sift_groundtruth.ivecs")
    logger.debug("successful load sift1M")
    return xb, xq, xt, gt


def load_sift10K(logger):
    xt = fvecs_read("siftsmall/siftsmall_learn.fvecs")
    xb = fvecs_read("siftsmall/siftsmall_base.fvecs")
    xq = fvecs_read("siftsmall/siftsmall_query.fvecs")
    gt = ivecs_read("siftsmall/siftsmall_groundtruth.ivecs")
    logger.debug("successful load sift10K")
    return xb, xq, xt, gt


def get_sift1M(logger):
    url = "ftp://ftp.irisa.fr"
    dirname = "local/texmex/corpus/"
    filename = "sift.tar.gz"
    host = get_ftp_ip(url)
    if download_sift(logger, host, dirname, "./", filename) == False:
        return
    untar(logger, filename, "./", "sift")
    xb, xq, xt, gt = load_sift1M(logger)
    return xb, xq, xt, gt


def get_sift10K(logger):
    url = "ftp://ftp.irisa.fr"
    dirname = "local/texmex/corpus/"
    filename = "siftsmall.tar.gz"
    host = get_ftp_ip(url)
    if download_sift(logger, host, dirname, "./", filename) == False:
        return
    untar(logger, filename, "./", "siftsmall")
    xb, xq, xt, gt = load_sift10K(logger)
    return xb, xq, xt, gt

def normalization(data):
    data[np.linalg.norm(data, axis=1) == 0] = 1.0 / np.sqrt(data.shape[1])
    data /= np.linalg.norm(data, axis=1)[:, np.newaxis]
    return data

class Dataset:
    def __init__(self, logger=None):
        self.d = -1
        self.metric = "L2"  # or InnerProduct
        self.nq = -1
        self.nb = -1
        self.nt = -1
        self.url = ""
        self.basedir = ""
        self.logger = logger

        self.download()

    def download(self):
        pass

    def get_database(self):
        pass

    def get_queries(self):
        pass

    def get_groundtruth(self):
        pass


class DatasetSift10K(Dataset):
    """
    Data from ftp://ftp.irisa.fr/local/texmex/corpus/siftsmall.tar.gz
    """

    def __init__(self, logger=None):
        self.d = 128
        self.metric = "L2"
        self.nq = 100
        self.nb = 10000
        self.nt = -1
        self.url = "ftp://ftp.irisa.fr"
        self.basedir = "datasets/"
        self.logger = logger

        self.download()

    def download(self):
        dirname = "local/texmex/corpus/"
        filename = "siftsmall.tar.gz"
        host = get_ftp_ip(self.url)
        if download_sift(self.logger, host, dirname, self.basedir, filename) == False:
            return
        untar(self.logger, filename, self.basedir, "siftsmall")

    def get_database(self):
        return fvecs_read(self.basedir + "siftsmall/siftsmall_base.fvecs")

    def get_queries(self):
        return fvecs_read(self.basedir + "siftsmall/siftsmall_query.fvecs")

    def get_groundtruth(self):
        return ivecs_read(self.basedir + "siftsmall/siftsmall_groundtruth.ivecs")


class DatasetSift1M(Dataset):
    """
    Data from ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz
    """

    def __init__(self, logger=None):
        self.d = 128
        self.metric = "L2"
        self.nq = 100
        self.nb = 10000
        self.nt = -1
        self.url = "ftp://ftp.irisa.fr"
        self.basedir = "datasets/"
        self.logger = logger

        self.download()

    def download(self):
        dirname = "local/texmex/corpus/"
        filename = "sift.tar.gz"
        host = get_ftp_ip(self.url)
        if download_sift(self.logger, host, dirname, self.basedir, filename) == False:
            return
        untar(self.logger, filename, self.basedir, "sift")

    def get_database(self):
        return fvecs_read(self.basedir + "sift/sift_base.fvecs")

    def get_queries(self):
        return fvecs_read(self.basedir + "sift/sift_query.fvecs")

    def get_groundtruth(self):
        return ivecs_read(self.basedir + "sift/sift_groundtruth.ivecs")


class DatasetGlove(Dataset):
    """
    Data from http://ann-benchmarks.com/glove-100-angular.hdf5
    """

    def __init__(self, logger=None):
        import h5py

        self.metric = "IP"
        self.d, self.nt = 100, 0

        self.url = "http://ann-benchmarks.com/glove-100-angular.hdf5"
        self.basedir = "datasets/glove/"
        self.logger = logger
        self.download()

        self.glove_h5py = h5py.File(self.basedir + "glove-100-angular.hdf5", "r")
        self.nb = self.glove_h5py["train"].shape[0]
        self.nq = self.glove_h5py["test"].shape[0]

    def download(self):
        import requests

        fname = self.basedir + "glove-100-angular.hdf5"
        if os.path.isfile(fname):
            self.logger.debug("%s exists, no need to download" % (fname))
            return
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(fname, "wb") as file:
                file.write(response.content)
        else:
            self.logger.error(
                f"Failed to download file. Response status code: {response.status_code}"
            )

    def get_queries(self):
        xq = np.array(self.glove_h5py["test"])
        return normalization(xq)

    def get_database(self):
        xb = np.array(self.glove_h5py["train"])
        return normalization(xb)

    def get_groundtruth(self):
        return self.glove_h5py["neighbors"]


class DatasetNytimes(Dataset):
    """
    Data from http://ann-benchmarks.com/nytimes-256-angular.hdf5
    """

    def __init__(self, logger=None):
        import h5py

        self.metric = "IP"
        self.d, self.nt = 100, 0

        self.url = "http://ann-benchmarks.com/nytimes-256-angular.hdf5"
        self.basedir = "datasets/nytimes/"
        self.logger = logger
        self.download()

        self.nytimes_h5py = h5py.File(self.basedir + "nytimes-256-angular.hdf5", "r")
        self.nb = self.nytimes_h5py["train"].shape[0]
        self.nq = self.nytimes_h5py["test"].shape[0]

    def download(self):
        import requests

        fname = self.basedir + "nytimes-256-angular.hdf5"
        if os.path.isfile(fname):
            self.logger.debug("%s exists, no need to download" % (fname))
            return
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(fname, "wb") as file:
                file.write(response.content)
        else:
            self.logger.error(
                f"Failed to download file. Response status code: {response.status_code}"
            )

    def get_queries(self):
        xq = np.array(self.nytimes_h5py["test"])
        return normalization(xq)

    def get_database(self):
        xb = np.array(self.nytimes_h5py["train"])
        if xb.dtype != np.float32:
            xb = xb.astype(np.float32)
        return normalization(xb)

    def get_groundtruth(self):
        return self.nytimes_h5py["neighbors"]


class DatasetMusic1M(Dataset):
    """
    Data from https://github.com/stanis-morozov/ip-nsw#dataset
    """

    def __init__(self):
        Dataset.__init__(self)
        self.d, self.nt, self.nb, self.nq = 100, 0, 10**6, 10000
        self.metric = "IP"
        self.basedir = "datasets/music/"

    def download(self):
        # TODO
        pass

    def get_database(self):
        xb = np.fromfile(self.basedir + "database_music100.bin", dtype="float32")
        xb = xb.reshape(-1, 100)
        return xb

    def get_queries(self):
        xq = np.fromfile(self.basedir + "query_music100.bin", dtype="float32")
        xq = xq.reshape(-1, 100)
        return xq

    def get_groundtruth(self):
        return np.load(self.basedir + "gt.npy")

def get_dataset_by_name(logger, name):
    if name == "sift":
        dataset = DatasetSift1M(logger)
        return dataset.get_database(), dataset.get_queries(), dataset.get_groundtruth()
    elif name == "siftsmall":
        dataset = DatasetSift10K(logger)
        return dataset.get_database(), dataset.get_queries(), dataset.get_groundtruth()
    elif name == "glove":
        dataset = DatasetGlove(logger)
        return dataset.get_database(), dataset.get_queries(), dataset.get_groundtruth()
    elif name == "nytimes":
        dataset = DatasetNytimes(logger)
        return dataset.get_database(), dataset.get_queries(), dataset.get_groundtruth()