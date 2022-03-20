FROM node:14-bullseye-slim as base

ARG CHANGE_SOURCE=false

RUN apt-get install -y apt-transport-https ca-certificates

RUN if [ ${CHANGE_SOURCE} = true ]; then \
    mv /etc/apt/sources.list /etc/apt/sources.list.bak; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free" > /etc/apt/sources.list; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free" >> /etc/apt/sources.list; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free" >> /etc/apt/sources.list; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list; \
    fi;

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    git \
    build-essential \
    python \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/frappe-bench
RUN mkdir -p sites/assets

ARG FRAPPE_VERSION
RUN git clone --depth 1 -b ${FRAPPE_VERSION} https://github.com/frappe/frappe apps/frappe



FROM base as frappe_prod_node_modules
RUN if [ ${CHANGE_SOURCE} = true ]; then \
    yarn config set registry https://registry.npm.taobao.org; \
    yarn config set sass_binary_site "https://cdn.npm.taobao.org/dist/node-sass/"; \
    fi;
# Install production node modules
RUN yarn --cwd apps/frappe --prod



FROM frappe_prod_node_modules as frappe_assets

# Install development node modules
RUN yarn --cwd apps/frappe

# Build assets they're stored in frappe-bench/sites/assets
RUN echo "frappe" >sites/apps.txt \
    && yarn --cwd apps/frappe run production \
    && rm sites/apps.txt \
    # TODO: Currently `yarn run production` doesn't create .build on develop branch: https://github.com/frappe/frappe/issues/15396
    && if [ ! -f sites/.build ]; then touch sites/.build; fi



FROM base as erpnext_prod_node_modules

ARG ERPNEXT_VERSION
RUN git clone --depth 1 -b ${ERPNEXT_VERSION} https://github.com/frappe/erpnext apps/erpnext
RUN git clone --depth 1 -b master https://gitee.com/yuzelin/erpnext_chinese.git apps/erpnext_chinese
RUN git clone --depth 1 -b master https://gitee.com/yuzelin/erpnext_oob.git apps/erpnext_oob

RUN yarn --cwd apps/erpnext --prod
RUN yarn --cwd apps/erpnext_chinese --prod
RUN yarn --cwd apps/erpnext_oob --prod

FROM erpnext_prod_node_modules as erpnext_assets

COPY --from=frappe_assets /root/frappe-bench/apps/frappe/node_modules /root/frappe-bench/apps/frappe/node_modules
COPY --from=frappe_assets /root/frappe-bench/apps/frappe/package.json /root/frappe-bench/apps/frappe/yarn.lock /root/frappe-bench/apps/frappe/

RUN echo "frappe\nerpnext\nerpnext_chinese\nerpnext_oob" >sites/apps.txt \
    && yarn --cwd apps/frappe run production --app erpnext \
    && yarn --cwd apps/frappe run production --app erpnext_chinese \
    && yarn --cwd apps/frappe run production --app erpnext_oob \
    && rm sites/apps.txt



FROM base as error_pages

RUN git clone --depth 1 https://github.com/frappe/bench /root/bench



FROM nginxinc/nginx-unprivileged:1.21.6-alpine as frappe

COPY --from=error_pages /root/bench/bench/config/templates/502.html /usr/share/nginx/html
COPY --from=base /root/frappe-bench/apps/frappe/frappe/public /usr/share/nginx/html/assets/frappe
COPY --from=frappe_prod_node_modules /root/frappe-bench/apps/frappe/node_modules /usr/share/nginx/html/assets/frappe/node_modules
COPY --from=frappe_assets /root/frappe-bench/sites /usr/share/nginx/html

# https://github.com/nginxinc/docker-nginx-unprivileged/blob/main/stable/alpine/20-envsubst-on-templates.sh
COPY nginx-template.conf /etc/nginx/templates/default.conf.template
# https://github.com/nginxinc/docker-nginx-unprivileged/blob/main/stable/alpine/docker-entrypoint.sh
COPY entrypoint.sh /docker-entrypoint.d/frappe-entrypoint.sh

USER 1000



FROM frappe as erpnext

COPY --from=erpnext_prod_node_modules /root/frappe-bench/apps/erpnext/erpnext/public /usr/share/nginx/html/assets/erpnext
COPY --from=erpnext_prod_node_modules /root/frappe-bench/apps/erpnext/node_modules /usr/share/nginx/html/assets/erpnext/node_modules
COPY --from=erpnext_prod_node_modules /root/frappe-bench/apps/erpnext_oob/erpnext_oob/public /usr/share/nginx/html/assets/erpnext_oob
COPY --from=erpnext_assets /root/frappe-bench/sites /usr/share/nginx/html
