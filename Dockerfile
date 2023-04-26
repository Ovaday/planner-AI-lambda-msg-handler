FROM public.ecr.aws/lambda/python:3.10

#all files are stored in var/task
RUN yum update -y && \
    yum install -y gcc-c++ make wget tar cmake3 openssl-devel gzip stat \
    flac-devel libogg-devel libvorbis-devel vorbis-tools alsa-lib-devel \
    opus-devel lame-devel libmpg123-devel pkgconfig epel-release sqlite-devel libsamplerate sox libsndio ffmpeg

RUN pip install --upgrade pip && \
    pip install awscli

RUN yum install -y xz which

RUN curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz && \
    tar -xf ffmpeg.tar.xz --strip-components=1 -C /usr/bin/ && \
    rm ffmpeg.tar.xz

#RUN yum -y install ffmpeg ffmpeg-devel &&
RUN which ffprobe && which ffmpeg

ENV PATH="${PATH}:/usr/bin/cmake3"


# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY ./tg_routine/requirements.txt  .
#RUN yum -y install libsndfile
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
#RUN python -m pip install --force-reinstall soundfile

# Copy function code
#COPY ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/DatabaseHelpers ${LAMBDA_TASK_ROOT}
ADD ./tg_routine/DatabaseHelpers/* ${LAMBDA_TASK_ROOT}/DatabaseHelpers/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]