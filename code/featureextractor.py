from nltk.compat import python_2_unicode_compatible

printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            # print("This is not a very good feature extractor!")
            printed = True

        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            # dependents = [a[2] for a in arcs if a[0] == token]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

            # POSTAG Stack 0
            if "tag" in token and FeatureExtractor._check_informative(token["tag"]):
                result.append("STK_0_POSTAG_" + token["tag"])

            # Coarse Tag
            # Minimal effect
            # if "ctag" in token and FeatureExtractor._check_informative(token["ctag"]):
            #     result.append("STK_0_CPOSTAG_" + token["ctag"])

            # ID
            # No effect
            # if "address" in token and FeatureExtractor._check_informative(token["address"]):
            #     result.append("STK_0_ID_" + str(token["address"]))

            # Dependents
            # if dependents:
            #     for dependent in dependents:
            #         result.append("STK_0_DEPENDENT_" + dependent)

        # POSTAG Stack 1
        if len(stack) > 1:
            stack_idx1 = stack[-2]
            token = tokens[stack_idx1]
            if FeatureExtractor._check_informative(token["tag"]):
                result.append("STK_1_TAG_" + token["tag"])

        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            # dependents = [a[2] for a in arcs if a[0] == token]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

            # POSTAG Buffer 0
            if "tag" in token and FeatureExtractor._check_informative(token["tag"]):
                result.append("BUF_0_POSTAG_" + token["tag"])

            # FOLLOWING_WORD Buffer 0
            # TODO: Refactor, this returns a syntax error
            # following_word = tokens[buffer_idx0 + 1]
            # if FeatureExtractor._check_informative(following_word['word'], True):
            #     result.append('BUF_0_FW_' + following_word['word'])

            # Coarse Tag
            # Minimal effect
            # if "ctag" in token and FeatureExtractor._check_informative(token["ctag"]):
            #     result.append("BUF_0_CPOSTAG_" + token["ctag"])

            # ID
            # No effect
            # if "address" in token and FeatureExtractor._check_informative(token["address"]):
            #     result.append("BUF_0_ID_" + str(token["address"]))

            # DEPS Buffer 0
            # TODO: Reimplement, useful
            if FeatureExtractor._check_informative(token["deps"], True):
                for dep in token["deps"]:
                    result.append("BUF_0_DEP_" + dep)

        # POSTAG Buffer 1
        if len(buffer) > 1:
            buffer_idx1 = buffer[1]
            token = tokens[buffer_idx1]
            if FeatureExtractor._check_informative(token["tag"]):
                result.append("BUF_1_TAG_" + token["tag"])

            # FORM Buffer 1
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_1_FORM_' + token['word'])

        # Tag 2
        # Note: Negative effect
        # if len(buffer) > 2:
        #     buffer_idx2 = buffer[2]
        #     token = tokens[buffer_idx2]
        #     if FeatureExtractor._check_informative(token["tag"]):
        #         result.append("BUF_2_TAG_" + token["tag"])

        # Distance
        if stack and buffer:
            stack_idx0 = stack[-1]
            stack_token = tokens[stack_idx0]
            stack_id = stack_token["address"]
            buffer_idx0 = buffer[0]
            buffer_token = tokens[buffer_idx0]
            buffer_id = buffer_token["address"]
            distance = buffer_id - stack_id
            result.append("DISTANCE_" + str(distance))

        # Intervening dependencies
        # Note: Negative effect
        # if arcs:
        #     existing_arcs = []
        #     for (wi, r, wj) in arcs:
        #         existing_arcs.append(r)
        #     for arc in set(existing_arcs):
        #         result.append("EXISTING_ARC_" + arc)

        return result
