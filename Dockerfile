FROM public.ecr.aws/lambda/python:3.10

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY ./tg_routine/requirements.txt  .
RUN yum -y install libsndfile
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN python -m pip install --force-reinstall soundfile


#all files are stored in var/task
RUN yum update -y && yum install gcc-c++ make wget tar openssl-devel gzip stat -y
RUN wget https://github.com/Kitware/CMake/releases/download/v3.24.0/cmake-3.24.0.tar.gz && \
    tar -zxvf cmake-3.24.0.tar.gz && \
    rm cmake-3.24.0.tar.gz
RUN cd cmake-3.24.0 && ./bootstrap -- -DCMAKE_USE_OPENSSL=OFF && make && make install && cd ..
RUN wget https://github.com/libsndfile/libsndfile/archive/refs/tags/1.1.0.tar.gz && \
    tar -zxvf 1.1.0.tar.gz && \
    rm 1.1.0.tar.gz && \
    mv libsndfile-1.1.0 ${LAMBDA_TASK_ROOT}/libsndfile
RUN cd libsndfile && cmake -G"Unix Makefiles" && make && make install && cd ..

# Copy function code
#COPY ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/DatabaseHelpers ${LAMBDA_TASK_ROOT}
ADD ./tg_routine/DatabaseHelpers/* ${LAMBDA_TASK_ROOT}/DatabaseHelpers/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]