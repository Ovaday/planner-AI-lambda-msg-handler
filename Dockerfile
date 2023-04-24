FROM public.ecr.aws/lambda/python:3.10

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY ./tg_routine/requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
#COPY ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/* ${LAMBDA_TASK_ROOT}/
ADD ./tg_routine/DatabaseHelpers ${LAMBDA_TASK_ROOT}
ADD ./tg_routine/DatabaseHelpers/* ${LAMBDA_TASK_ROOT}/DatabaseHelpers/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]