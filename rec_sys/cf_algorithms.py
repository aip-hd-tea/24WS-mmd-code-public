# Artur Andrzejak, October 2024
# Algorithms for collaborative filtering

import numpy as np


def complete_code(message):
    raise Exception(f"Please complete the code: {message}")
    return None


def center_and_nan_to_zero(matrix, axis=0):
    """Center the matrix and replace nan values with zeros"""
    # Compute along axis 'axis' the mean of non-nan values
    # E.g. axis=0: mean of each column, since op is along rows (axis=0)
    means = np.nanmean(matrix, axis=axis)
    # Subtract the mean from each axis
    matrix_centered = matrix - means
    return np.nan_to_num(matrix_centered)


def cosine_sim(u, v):
    dot = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cosine_sim = dot / (norm_u * norm_v)
    return cosine_sim


def fast_cosine_sim(utility_matrix, vector, axis=0):
    """Compute the cosine similarity between the matrix and the vector"""
    # Compute the norms of each column
    norms = np.linalg.norm(utility_matrix, axis=axis)
    um_normalized = utility_matrix / norms
    # Compute the dot product of transposed normalized matrix and the vector
    dot = np.dot(um_normalized.T, vector)
    norm_vector = np.linalg.norm(vector)
    # Scale by the vector norm
    scaled = dot / norm_vector
    return scaled


# Implement the CF from the lecture 1
def rate_all_items(orig_utility_matrix, user_index, neighborhood_size):
    print(
        f"\n>>> CF computation for UM w/ shape: "
        + f"{orig_utility_matrix.shape}, user_index: {user_index}, neighborhood_size: {neighborhood_size}\n"
    )

    clean_utility_matrix = center_and_nan_to_zero(orig_utility_matrix)
    """ Compute the rating of all items not yet rated by the user"""
    user_col = clean_utility_matrix[:, user_index]
    # Compute the cosine similarity between the user and all other users
    similarities = fast_cosine_sim(clean_utility_matrix, user_col)

    def rate_one_item(item_index):
        # If the user has already rated the item, return the rating
        if not np.isnan(orig_utility_matrix[item_index, user_index]):
            return orig_utility_matrix[item_index, user_index]

        # Find the indices of users who rated the item
        users_who_rated = np.where(
            np.isnan(orig_utility_matrix[item_index, :]) == False
        )[0]
        # From those, get indices of users with the highest similarity (watch out: result indices are rel. to users_who_rated)
        best_among_who_rated = np.argsort(similarities[users_who_rated])
        # Select top neighborhood_size of them
        best_among_who_rated = best_among_who_rated[-neighborhood_size:]
        # Convert the indices back to the original utility matrix indices
        best_among_who_rated = users_who_rated[best_among_who_rated]
        # Retain only those indices where the similarity is not nan
        best_among_who_rated = best_among_who_rated[
            np.isnan(similarities[best_among_who_rated]) == False
        ]
        if best_among_who_rated.size > 0:
            # Compute the rating of the item
            sum_similarities = np.sum(np.abs(similarities[best_among_who_rated]))
            bawr_similarities = similarities[best_among_who_rated]
            bawr_ratings_item = orig_utility_matrix[item_index, best_among_who_rated]
            rating_of_item = (
                np.sum(bawr_similarities * (bawr_ratings_item)) / sum_similarities
            )
        else:
            rating_of_item = np.nan
        print(
            f"item_idx: {item_index}, neighbors: {best_among_who_rated}, rating: {rating_of_item}"
        )
        return rating_of_item

    num_items = orig_utility_matrix.shape[0]

    # Get all ratings
    ratings = list(map(rate_one_item, range(num_items)))
    return ratings


matrix = np.asarray(
    [
        [1.0, np.nan, 3.0, np.nan, np.nan, 5.0],
        [np.nan, np.nan, 5.0, 4.0, np.nan, np.nan],
        [2.0, 4.0, np.nan, 1.0, 2.0, np.nan],
        [np.nan, 2.0, 4.0, np.nan, 5.0, np.nan],
        [np.nan, np.nan, 4.0, 3.0, 4.0, 2.0],
        [1.0, np.nan, 3.0, np.nan, 3.0, np.nan],
    ]
)
print(rate_all_items(matrix, 0, 2))