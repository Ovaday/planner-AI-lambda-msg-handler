FROM public.ecr.aws/lambda/python:3.10

RUN yum update -y && \
    yum install -y wget tar openssl-devel gzip xz

RUN curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz && \
    tar -xf ffmpeg.tar.xz --strip-components=1 -C /usr/bin/ && \
    rm ffmpeg.tar.xz


# Install the function's dependencies using file requirements.txt from the project folder.
COPY ./tg_routine/requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
ADD ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/DatabaseHelpers ${LAMBDA_TASK_ROOT}
ADD ./tg_routine/DatabaseHelpers/* ${LAMBDA_TASK_ROOT}/DatabaseHelpers/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]